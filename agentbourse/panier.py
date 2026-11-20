"""Panier d'actions filtré par nos propres règles, pour la simulation.

On part des N plus grosses actions du fonds iShares MSCI World Islamic (déjà triées par MSCI),
et on retire celles que l'ONU cite (Gaza, colonies). On compare ensuite deux paniers construits
EXACTEMENT de la même façon : « complet » (les N actions) et « filtré » (sans les actions citées).

⚠️ Biais : on prend la composition d'AUJOURD'HUI et on la fait remonter jusqu'en 2015. Ça avantage
les deux paniers (on choisit après coup les entreprises qui ont réussi). Seul l'ÉCART entre les deux
paniers a du sens, pas leur résultat absolu.
"""
from dataclasses import dataclass

import pandas as pd

from agentbourse import config, etf, onu


@dataclass
class Action:
    symbole: str
    nom: str
    poids: float      # en %
    devise: str
    citations: list   # citations de l'ONU (vide si aucune)


def composer() -> list[Action]:
    """Les N plus grosses actions du fonds, avec pour chacune les citations de l'ONU."""
    fonds = config.FONDS_ISLAMIQUES[config.PANIER_FONDS]
    lignes = sorted((l for l in etf.lire(config.PANIER_FONDS, fonds) if l.symbole),
                    key=lambda l: l.poids, reverse=True)[: config.PANIER_NB_ACTIONS]
    liste_onu = onu.charger()
    return [Action(l.symbole, l.nom.title(), l.poids, l.devise, onu.citations(l.symbole, l.nom, liste_onu))
            for l in lignes]


def indice(rendements: pd.DataFrame, poids: dict[str, float]) -> pd.Series:
    """Cours d'un panier (base 100), à partir des rendements quotidiens de chaque action.

    Chaque jour, le rendement du panier = moyenne des rendements, pondérée par les poids.
    Une action pas encore cotée (ex. entrée en bourse en 2020) est ignorée jusqu'à sa cotation :
    les poids des autres sont alors agrandis pour faire 100 %.
    """
    colonnes = [s for s in poids if s in rendements.columns]
    r = rendements[colonnes]
    p = pd.Series({s: poids[s] for s in colonnes})
    presents = r.notna()
    poids_du_jour = presents.mul(p, axis=1)
    total = poids_du_jour.sum(axis=1)
    rendement_panier = (r.fillna(0) * poids_du_jour).sum(axis=1) / total.where(total > 0)
    return 100 * (1 + rendement_panier.fillna(0)).cumprod()


def rendements_eur(actions: list[Action]) -> pd.DataFrame:
    """Rendements quotidiens en euros, dividendes réinvestis (besoin d'internet)."""
    import yfinance as yf

    debut = config.SIMULATION_DEBUT
    cours = yf.download([a.symbole for a in actions], start=debut, auto_adjust=True,
                        progress=False)["Close"]
    cours.index = cours.index.tz_localize(None).normalize()
    devises = {a.devise for a in actions if a.devise and a.devise != "EUR"}
    changes = {}
    for d in devises:  # combien d'unités de la devise pour 1 €
        c = yf.Ticker(f"EUR{d}=X").history(start=debut)["Close"]
        c.index = c.index.tz_localize(None).normalize()
        changes[d] = c.reindex(cours.index).ffill().bfill()
    en_eur = pd.DataFrame({a.symbole: cours[a.symbole] / changes.get(a.devise, 1.0)
                           for a in actions if a.symbole in cours.columns})
    # Jours fériés différents selon les bourses : on reprend le dernier cours connu.
    return en_eur.ffill().pct_change(fill_method=None)


def deux_paniers(actions: list[Action], rendements: pd.DataFrame) -> dict[str, pd.Series]:
    complet = {a.symbole: a.poids for a in actions}
    filtre = {a.symbole: a.poids for a in actions if not a.citations}
    return {
        f"Panier complet ({len(complet)} actions)": indice(rendements, complet),
        f"Panier sans les actions citées par l'ONU ({len(filtre)} actions)": indice(rendements, filtre),
    }
