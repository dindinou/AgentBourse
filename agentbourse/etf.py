"""Deuxième avis : l'action est-elle gardée par de vrais fonds islamiques (ETF) ?

Ces fonds utilisent des données payantes, plus complètes que les nôtres.
"""
import csv
import difflib
import re
import time
import unicodedata
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

from agentbourse import config

DOSSIER = Path(__file__).parent.parent / "donnees_etf"

# Bourse (nom iShares) -> fin du code Yahoo.
SUFFIXES = {
    "New York Stock Exchange Inc.": "", "NASDAQ": "", "Cboe BZX formerly known as BATS": "",
    "Tokyo Stock Exchange": ".T", "Toronto Stock Exchange": ".TO", "London Stock Exchange": ".L",
    "Nyse Euronext - Euronext Paris": ".PA", "Xetra": ".DE", "Asx - All Markets": ".AX",
    "SIX Swiss Exchange": ".SW", "Euronext Amsterdam": ".AS", "Borsa Italiana": ".MI",
    "Hong Kong Exchanges And Clearing Ltd": ".HK", "Bolsa De Madrid": ".MC",
    "Singapore Exchange": ".SI", "Omx Nordic Exchange Copenhagen A/S": ".CO",
    "Nasdaq Omx Helsinki Ltd.": ".HE", "Tel Aviv Stock Exchange": ".TA", "Oslo Bors Asa": ".OL",
    "Nasdaq Omx Nordic": ".ST", "Euronext Brussels": ".BR",
    "Saudi Stock Exchange": ".SR", "Bursa Malaysia": ".KL", "National Stock Exchange Of India": ".NS",
    "Shanghai Stock Exchange": ".SS", "Shenzhen Stock Exchange": ".SZ", "Korea Exchange (Stock Market)": ".KS",
    "Taiwan Stock Exchange": ".TW", "Gretai Securities Market": ".TWO", "Johannesburg Stock Exchange": ".JO",
    "Bolsa Mexicana De Valores": ".MX", "Stock Exchange Of Thailand": ".BK", "Qatar Exchange": ".QA",
    "Dubai Financial Market": ".AE", "Abu Dhabi Securities Exchange": ".AE", "Kuwait Stock Exchange": ".KW",
    "Istanbul Stock Exchange": ".IS", "Indonesia Stock Exchange": ".JK", "XBSP": ".SA",
    "Warsaw Stock Exchange/Equities/Main Market": ".WA", "Athens Exchange S.A. Cash Market": ".AT",
    "Santiago Stock Exchange": ".SN", "Budapest Stock Exchange": ".BD", "Prague Stock Exchange": ".PR",
    "Philippine Stock Exchange Inc.": ".PS",
}

_MOTS_INUTILES = r"\b(inc|corp|corporation|co|company|ltd|limited|plc|sa|se|ag|nv|ab|asa|spa|tbk|bhd|berhad|" \
                 r"holdings?|group|class [a-z]|the)\b"


@dataclass
class Ligne:
    """Une action dans un fonds."""
    symbole: str | None   # code Yahoo, si on sait le calculer
    nom: str
    poids: float = 0.0    # part du fonds, en % (fichiers iShares seulement)
    devise: str = ""      # devise de cotation (fichiers iShares seulement)


@dataclass
class AvisFonds:
    gardee_par: list[str] = field(default_factory=list)   # noms des fonds islamiques qui la gardent
    dans_un_indice: bool = False                            # présente dans un indice « normal » suivi

    @property
    def statut(self) -> str:
        if self.gardee_par:
            return "gardee"
        return "ecartee" if self.dans_un_indice else "non_couverte"


def nom_simplifie(nom: str) -> str:
    nom = unicodedata.normalize("NFKD", nom).encode("ascii", "ignore").decode().lower()
    nom = re.sub(r"[^a-z0-9 ]", " ", nom)
    return " ".join(re.sub(_MOTS_INUTILES, " ", nom).split())


def symbole_yahoo(code: str, bourse: str) -> str | None:
    suffixe = SUFFIXES.get(bourse)
    if suffixe is None:
        return None
    code = code.strip().rstrip(".").replace(" ", "-").replace(".", "-")  # NOVO B -> NOVO-B, TECK.B -> TECK-B
    if suffixe == ".HK":
        code = code.zfill(4)
    if suffixe == ".KL" and not code.isdigit():
        return None  # en Malaisie, iShares donne un nom (TENAGA), Yahoo un numéro (5347) : on comparera les noms
    return code + suffixe


def telecharger(cle: str, fonds: dict) -> Path:
    """Télécharge la composition d'un fonds si elle manque ou est trop vieille."""
    chemin = DOSSIER / f"{cle}.csv"
    age_max = config.ETF_RAFRAICHIR_APRES_JOURS * 86400
    if chemin.exists() and time.time() - chemin.stat().st_mtime < age_max:
        return chemin
    DOSSIER.mkdir(exist_ok=True)
    requete = urllib.request.Request(fonds["url"], headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(requete, timeout=60) as reponse:
        contenu = reponse.read()
    if b"<html" in contenu[:500].lower():
        raise RuntimeError(f"Le site de {fonds['nom']} n'a pas renvoyé de fichier : adresse à mettre à jour.")
    chemin.write_bytes(contenu)
    return chemin


def lire(cle: str, fonds: dict) -> list[Ligne]:
    texte = telecharger(cle, fonds).read_text(encoding="utf-8-sig")
    lignes = texte.splitlines()
    if fonds["format"] == "spfunds":
        return [Ligne(l["StockTicker"].replace(".", "-"), l["SecurityName"])
                for l in csv.DictReader(lignes) if l.get("StockTicker")]
    debut = next(i for i, l in enumerate(lignes) if l.startswith("Ticker,"))
    return [Ligne(symbole_yahoo(l["Ticker"], l["Exchange"]), l["Name"],
                  float(l["Weight (%)"].replace("’", "").replace(",", "") or 0), l["Market Currency"])
            for l in csv.DictReader(lignes[debut:]) if l.get("Asset Class") == "Equity" and l.get("Ticker")]


def _present(symbole: str, nom: str, lignes: list[Ligne], noms: list[str]) -> bool:
    if any(l.symbole == symbole for l in lignes):
        return True
    # Pas trouvé par le code : on compare les noms (très ressemblants seulement).
    return bool(difflib.get_close_matches(nom_simplifie(nom), noms, n=1, cutoff=0.9))


class Fonds:
    """Charge une fois toutes les compositions, puis répond vite pour chaque action."""

    def __init__(self):
        self.islamiques = {f["nom"]: lire(cle, f) for cle, f in config.FONDS_ISLAMIQUES.items()}
        self.parents = [lire(cle, f) for cle, f in config.INDICES_PARENTS.items()]
        self._noms = {id(l): [nom_simplifie(x.nom) for x in l]
                      for l in [*self.islamiques.values(), *self.parents]}

    def avis(self, symbole: str, nom: str) -> AvisFonds:
        avis = AvisFonds()
        for nom_fonds, lignes in self.islamiques.items():
            if _present(symbole, nom, lignes, self._noms[id(lignes)]):
                avis.gardee_par.append(nom_fonds)
        avis.dans_un_indice = any(_present(symbole, nom, l, self._noms[id(l)]) for l in self.parents)
        return avis
