"""Indice AgentBourse : nos règles transformées en une liste d'actions avec leurs poids.

- Entrée : actions des fonds islamiques iShares (monde + émergents) dont notre résultat final est
  « unanimité » ou « avis majoritaire » (AAOIFI, fonds islamique, pas citée par l'ONU, aucune alerte).
- Poids : selon la valeur en bourse, plafonnés à 5 %.
- Portefeuille : chaque ligne est gardée en EUROS (pas en nombre de parts). Chaque jour, on la
  multiplie par la variation du cours « dividendes réinvestis », convertie en euros.
"""
import csv
import json
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass
from pathlib import Path

import pandas as pd

from agentbourse import alertes, config, conformite, donnees, etf, onu

DOSSIER = Path(__file__).parent.parent / "indice"
COMPOSITION = DOSSIER / "composition.csv"
ETAT = DOSSIER / "etat.json"
HISTORIQUE = DOSSIER / "historique.csv"
JOURNAL = DOSSIER / "journal.md"


@dataclass
class Ligne:
    symbole: str
    nom: str
    devise: str           # devise de cotation
    capitalisation_eur: float
    niveau: str
    poids: float = 0.0


# --- Poids --------------------------------------------------------------------------------------
def poids_plafonnes(tailles: dict[str, float], plafond: float) -> dict[str, float]:
    """Poids proportionnels aux tailles, aucun au-dessus du plafond (le surplus va aux autres)."""
    tailles = {s: t for s, t in tailles.items() if t and t > 0}
    if not tailles:
        return {}
    if len(tailles) * plafond <= 1:  # trop peu d'actions pour respecter le plafond : parts égales
        return {s: 1 / len(tailles) for s in tailles}
    plafonnes: set[str] = set()
    while True:
        reste = 1 - plafond * len(plafonnes)
        libres = {s: t for s, t in tailles.items() if s not in plafonnes}
        total = sum(libres.values())
        poids = {s: plafond for s in plafonnes} | {s: reste * t / total for s, t in libres.items()}
        trop = {s for s, p in poids.items() if p > plafond + 1e-12}
        if not trop:
            return poids
        plafonnes |= trop


def appliquer_poids(lignes: list[Ligne]) -> list[Ligne]:
    poids = poids_plafonnes({l.symbole: l.capitalisation_eur for l in lignes}, config.INDICE_PLAFOND)
    gardees = [l for l in lignes if l.symbole in poids]
    for l in gardees:
        l.poids = poids[l.symbole]
    return sorted(gardees, key=lambda l: l.poids, reverse=True)


# --- Sélection (réajustement trimestriel, long : ~800 actions) ----------------------------------
def univers() -> list[etf.Ligne]:
    vues, actions = set(), []
    for cle in config.INDICE_FONDS_UNIVERS:
        for l in etf.lire(cle, config.FONDS_ISLAMIQUES[cle]):
            if l.symbole and l.symbole not in vues:
                vues.add(l.symbole)
                actions.append(l)
    return actions


def examiner(symbole: str, fonds: etf.Fonds, liste_onu: list[dict]) -> tuple[Ligne | None, str]:
    """Analyse complète d'une action. Renvoie (ligne si elle entre dans l'indice, résultat final)."""
    chiffres = None
    for essai in range(config.INDICE_ESSAIS):
        try:
            chiffres = donnees.charger(symbole)
            break
        except Exception as erreur:
            if "Rate" not in type(erreur).__name__ and "Too Many" not in str(erreur):
                return None, "erreur de données"
            time.sleep(config.INDICE_PAUSE_SECONDES * (essai + 1))  # Yahoo freine : on attend de plus en plus
    if chiffres is None:
        return None, "erreur de données"
    niveau_calcule, _, _ = conformite.analyser(chiffres)
    liste_alertes = alertes.detecter(chiffres.activite, chiffres.description)
    avis = fonds.avis(chiffres.symbole, chiffres.nom)
    citations = onu.citations(chiffres.symbole, chiffres.nom, liste_onu)
    niveau = conformite.niveau_final(niveau_calcule, liste_alertes, avis.statut, bool(citations))
    if niveau not in config.INDICE_NIVEAUX_ADMIS or not chiffres.capitalisation:
        return None, niveau
    taux = donnees.taux_change(chiffres.devise, "EUR")
    if not taux:
        return None, "taux de change introuvable"
    return Ligne(chiffres.symbole, chiffres.nom, chiffres.devise_cours or chiffres.devise,
                 chiffres.capitalisation * taux, niveau), niveau


def selectionner(fonds: etf.Fonds, liste_onu: list[dict], afficher=print) -> tuple[list[Ligne], dict[str, int]]:
    actions = univers()
    afficher(f"Analyse de {len(actions)} actions…")
    with ThreadPoolExecutor(config.INDICE_ANALYSES_EN_PARALLELE) as pool:
        resultats = list(pool.map(lambda a: examiner(a.symbole, fonds, liste_onu), actions))
    bilan: dict[str, int] = {}
    for _, niveau in resultats:
        bilan[niveau] = bilan.get(niveau, 0) + 1
    return appliquer_poids([l for l, _ in resultats if l]), bilan


# --- Valeur du portefeuille ---------------------------------------------------------------------
def reequilibrer(positions: dict[str, float], poids: dict[str, float], frais: float) -> tuple[dict[str, float], float]:
    """Remet chaque ligne à son poids cible. Renvoie (nouvelles positions, frais payés)."""
    total = sum(positions.values())
    echanges = sum(abs(total * poids.get(s, 0) - positions.get(s, 0)) for s in set(poids) | set(positions))
    frais_payes = echanges * frais
    reste = total - frais_payes
    return {s: reste * p for s, p in poids.items()}, frais_payes


def faire_evoluer(positions: dict[str, float], variations: dict[str, float]) -> dict[str, float]:
    """Applique la variation de chaque action (1.02 = +2 %). Sans cours connu : pas de changement."""
    return {s: v * variations.get(s, 1.0) for s, v in positions.items()}


def variations_eur(lignes: list[Ligne], depuis: str) -> tuple[dict[str, float], str]:
    """Variation en euros de chaque action entre la date `depuis` et le dernier cours connu."""
    import yfinance as yf

    debut = (pd.Timestamp(depuis) - pd.Timedelta(days=10)).date().isoformat()
    cours = yf.download([l.symbole for l in lignes], start=debut, auto_adjust=True, progress=False)["Close"]
    cours.index = cours.index.tz_localize(None).normalize()
    cours = cours.ffill()
    jour_depart = cours.index[cours.index <= pd.Timestamp(depuis)].max()
    dernier = cours.index.max()
    variations = {}
    changes = {}
    for l in lignes:
        if l.symbole not in cours or pd.isna(cours.at[jour_depart, l.symbole]):
            continue
        devise = l.devise
        if devise not in changes:
            changes[devise] = _change_eur(devise, debut, cours.index)
        c = cours[l.symbole] / changes[devise]
        if pd.notna(c.at[dernier]) and pd.notna(c.at[jour_depart]):
            variations[l.symbole] = float(c.at[dernier] / c.at[jour_depart])
    return variations, dernier.date().isoformat()


def _change_eur(devise: str, debut: str, jours) -> pd.Series:
    """Unités de la devise pour 1 € (1 si la devise est l'euro)."""
    import yfinance as yf

    if devise in ("EUR", ""):
        return pd.Series(1.0, index=jours)
    c = yf.Ticker(f"EUR{devise}=X").history(start=debut)["Close"]
    c.index = c.index.tz_localize(None).normalize()
    return c.reindex(jours).ffill().bfill()


# --- Fichiers -----------------------------------------------------------------------------------
def lire_composition() -> list[Ligne]:
    if not COMPOSITION.exists():
        return []
    with open(COMPOSITION, encoding="utf-8") as f:
        return [Ligne(l["symbole"], l["nom"], l["devise"], float(l["capitalisation_eur"]), l["niveau"],
                      float(l["poids"])) for l in csv.DictReader(f)]


def ecrire_composition(lignes: list[Ligne]) -> None:
    DOSSIER.mkdir(exist_ok=True)
    with open(COMPOSITION, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(asdict(lignes[0])))
        w.writeheader()
        w.writerows(asdict(l) for l in lignes)


def lire_etat() -> dict | None:
    return json.loads(ETAT.read_text(encoding="utf-8")) if ETAT.exists() else None


def ecrire_etat(etat: dict) -> None:
    DOSSIER.mkdir(exist_ok=True)
    ETAT.write_text(json.dumps(etat, indent=1, ensure_ascii=False), encoding="utf-8")


def ajouter_historique(date: str, portefeuille: float, indice: float, nb_actions: int) -> None:
    nouveau = not HISTORIQUE.exists()
    with open(HISTORIQUE, "a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        if nouveau:
            w.writerow(["date", "portefeuille_eur", "indice_base_100", "nb_actions"])
        w.writerow([date, round(portefeuille, 2), round(indice, 4), nb_actions])


def ecrire_journal(date: str, lignes_texte: list[str]) -> None:
    DOSSIER.mkdir(exist_ok=True)
    nouveau = not JOURNAL.exists()
    with open(JOURNAL, "a", encoding="utf-8") as f:
        if nouveau:
            f.write("# Journal de l'agent AgentBourse\n\nArgent fictif uniquement. Pas un conseil en investissement.\n")
        f.write(f"\n## {date}\n\n" + "\n".join(f"- {l}" for l in lignes_texte) + "\n")
