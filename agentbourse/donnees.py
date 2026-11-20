"""Récupère les chiffres d'une entreprise sur Yahoo Finance (besoin d'internet)."""
import math

import yfinance as yf

from agentbourse.conformite import Chiffres

# Devises cotées en centimes : Yahoo donne le prix en pence (GBp), agorot (ILA)…
_CENTIMES = {"GBp": ("GBP", 100), "GBX": ("GBP", 100), "ILA": ("ILS", 100), "ZAc": ("ZAR", 100)}


def _premiere_valeur(tableau, lignes: list[str]) -> float | None:
    """Prend la valeur la plus récente de la première ligne trouvée dans le tableau."""
    if tableau is None or tableau.empty:
        return None
    for ligne in lignes:
        if ligne in tableau.index:
            for valeur in tableau.loc[ligne]:  # colonnes = années, la plus récente d'abord
                if valeur is not None and not math.isnan(valeur):
                    return float(valeur)
    return None


def _revenus_interets(resultats) -> float | None:
    """Revenus d'intérêts. Si Yahoo ne les donne pas, on les retrouve :
    intérêts nets = intérêts reçus - intérêts payés, donc intérêts reçus = nets + payés."""
    direct = _premiere_valeur(resultats, ["Interest Income", "Interest Income Non Operating"])
    if direct is not None:
        return direct
    nets = _premiere_valeur(resultats, ["Net Interest Income", "Net Non Operating Interest Income Expense"])
    payes = _premiere_valeur(resultats, ["Interest Expense", "Interest Expense Non Operating"])
    if nets is None or payes is None:
        return None
    return max(nets + abs(payes), 0.0)


def _taux_change(de: str, vers: str) -> float | None:
    if de == vers:
        return 1.0
    historique = yf.Ticker(f"{de}{vers}=X").history(period="5d")
    if historique.empty:
        return None
    return float(historique["Close"].iloc[-1])


def charger(symbole: str) -> Chiffres:
    action = yf.Ticker(symbole)
    info = action.info or {}

    devise_cours = info.get("currency") or ""
    facteur = 1
    if devise_cours in _CENTIMES:
        devise_cours, facteur = _CENTIMES[devise_cours]
    devise_comptes = info.get("financialCurrency") or devise_cours
    # La capitalisation est dans la devise du cours : on la met dans celle des comptes.
    taux = _taux_change(devise_cours, devise_comptes) if devise_cours else None

    capitalisation = info.get("marketCap")
    capitalisation = capitalisation * taux if capitalisation and taux else None

    capitalisation_36_mois = None
    actions_en_circulation = info.get("sharesOutstanding")
    historique = action.history(period="3y")
    if actions_en_circulation and taux and not historique.empty:
        prix_moyen = float(historique["Close"].mean()) / facteur
        capitalisation_36_mois = prix_moyen * actions_en_circulation * taux

    bilan = action.balance_sheet
    resultats = action.income_stmt

    # Trésorerie au sens de l'AAOIFI : argent + placements à intérêt, à court ET à long terme.
    # Les parts dans d'autres entreprises (filiales, coentreprises) ne comptent pas.
    tresorerie = _premiere_valeur(bilan, [
        "Cash Cash Equivalents And Short Term Investments",
        "Cash And Cash Equivalents",
    ])
    placements_long_terme = _premiere_valeur(bilan, ["Investmentin Financial Assets"])
    if tresorerie is not None and placements_long_terme is not None:
        tresorerie += placements_long_terme
    return Chiffres(
        symbole=symbole.upper(),
        nom=info.get("longName") or info.get("shortName") or symbole,
        secteur=info.get("sector") or "",
        activite=info.get("industry") or "",
        pays=info.get("country") or "",
        devise=devise_comptes,
        capitalisation=capitalisation,
        capitalisation_36_mois=capitalisation_36_mois,
        actifs=_premiere_valeur(bilan, ["Total Assets"]),
        dette=_premiere_valeur(bilan, ["Total Debt"]),
        tresorerie=tresorerie,
        revenus_interets=_revenus_interets(resultats),
        chiffre_affaires=_premiere_valeur(resultats, ["Total Revenue", "Operating Revenue"]),
        description=info.get("longBusinessSummary") or "",
    )
