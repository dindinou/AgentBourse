"""Trouver une action à partir d'un nom tapé par quelqu'un, même mal écrit."""
import difflib
from dataclasses import dataclass

from agentbourse import config


@dataclass
class Proposition:
    symbole: str
    nom: str
    bourse: str = ""


# Grandes entreprises connues : sert à corriger les fautes (« aple » -> Apple),
# que la recherche Yahoo ne corrige pas toujours. Liste à compléter.
ACTIONS_CONNUES = {
    "apple": ("AAPL", "Apple Inc."),
    "microsoft": ("MSFT", "Microsoft"),
    "nvidia": ("NVDA", "Nvidia"),
    "google": ("GOOGL", "Alphabet (Google)"),
    "alphabet": ("GOOGL", "Alphabet (Google)"),
    "amazon": ("AMZN", "Amazon"),
    "tesla": ("TSLA", "Tesla"),
    "meta": ("META", "Meta (Facebook)"),
    "facebook": ("META", "Meta (Facebook)"),
    "netflix": ("NFLX", "Netflix"),
    "samsung": ("005930.KS", "Samsung Electronics"),
    "toyota": ("7203.T", "Toyota"),
    "nestle": ("NESN.SW", "Nestlé"),
    "asml": ("ASML.AS", "ASML"),
    "sap": ("SAP.DE", "SAP"),
    "lvmh": ("MC.PA", "LVMH"),
    "totalenergies": ("TTE.PA", "TotalEnergies"),
    "airbus": ("AIR.PA", "Airbus"),
    "loreal": ("OR.PA", "L'Oréal"),
    "danone": ("BN.PA", "Danone"),
    "hermes": ("RMS.PA", "Hermès"),
    "schneider": ("SU.PA", "Schneider Electric"),
    "aramco": ("2222.SR", "Saudi Aramco"),
    "sabic": ("2010.SR", "SABIC"),
    "stc": ("7010.SR", "Saudi Telecom (stc)"),
    "almarai": ("2280.SR", "Almarai"),
    "emaar": ("EMAAR.AE", "Emaar Properties"),
    "petronas": ("5681.KL", "Petronas Dagangan"),
    "tenaga": ("5347.KL", "Tenaga Nasional"),
    "telkom": ("TLKM.JK", "Telkom Indonesia"),
    "bimas": ("BIMAS.IS", "BIM (Turquie)"),
}


def _normaliser(texte: str) -> str:
    remplacements = str.maketrans("éèêëàâäîïôöûüç'’", "eeeeaaaiioouuc  ")
    return texte.lower().translate(remplacements).replace(" ", "")


def depuis_liste_connue(texte: str) -> list[Proposition]:
    """Noms connus qui ressemblent au texte tapé (corrige les fautes de frappe)."""
    cles = difflib.get_close_matches(_normaliser(texte), ACTIONS_CONNUES,
                                     n=config.NB_PROPOSITIONS, cutoff=config.SIMILARITE_MIN)
    return [Proposition(*ACTIONS_CONNUES[c]) for c in cles]


def depuis_yahoo(texte: str) -> list[Proposition]:
    """Recherche sur Yahoo Finance (besoin d'internet). Ne garde que les actions."""
    import yfinance as yf

    try:
        resultats = yf.Search(texte, max_results=config.NB_PROPOSITIONS * 2).quotes
    except Exception:  # pas d'internet, Yahoo indisponible… on se contente de la liste connue
        return []
    return [
        Proposition(r["symbol"], r.get("longname") or r.get("shortname") or r["symbol"], r.get("exchange", ""))
        for r in resultats
        if r.get("quoteType") == "EQUITY" and r.get("symbol")
    ]


def chercher(texte: str) -> list[Proposition]:
    """Propositions sans doublon : d'abord les noms connus, puis Yahoo."""
    propositions, deja_vus = [], set()
    for p in depuis_liste_connue(texte) + depuis_yahoo(texte):
        if p.symbole not in deja_vus:
            deja_vus.add(p.symbole)
            propositions.append(p)
    return propositions[: config.NB_PROPOSITIONS]
