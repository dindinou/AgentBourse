"""Critère éthique : l'entreprise est-elle citée par l'ONU pour Gaza ou les colonies israéliennes ?

Liste dans donnees_onu/entreprises.csv, recopiée à la main des documents officiels de l'ONU :
  - rapport A/HRC/59/23 de la rapporteuse spéciale Francesca Albanese (juillet 2025) ;
  - base de données des entreprises actives dans les colonies, annexe I de A/HRC/60/19 (septembre 2025).
"""
import csv
from dataclasses import dataclass
from pathlib import Path

from agentbourse.etf import nom_simplifie

FICHIER = Path(__file__).parent.parent / "donnees_onu" / "entreprises.csv"


@dataclass
class Citation:
    nom: str
    source: str
    reference: str


def charger() -> list[dict]:
    with open(FICHIER, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _meme_entreprise(nom_liste: str, nom_action: str) -> bool:
    """Même nom, ou nom de l'action qui commence par le nom de la liste (s'il a au moins 2 mots).

    « Bank Leumi le-Israel B.M. » correspond à « Bank Leumi Le-Israel Ltd. ».
    Un nom d'un seul mot (« Egis ») doit être identique, pour ne pas toucher une autre entreprise.
    """
    a, b = nom_simplifie(nom_liste), nom_simplifie(nom_action)
    if not a or not b:
        return False
    if a == b:
        return True
    return len(a.split()) >= 2 and (b + " ").startswith(a + " ")


def citations(symbole: str, nom: str, liste: list[dict] | None = None) -> list[Citation]:
    """Toutes les fois où l'ONU cite cette entreprise (vide si jamais)."""
    trouvees = []
    for ligne in liste if liste is not None else charger():
        codes = [c.strip().upper() for c in ligne["codes_yahoo"].split(";") if c.strip()]
        if symbole.upper() in codes or _meme_entreprise(ligne["nom"], nom):
            trouvees.append(Citation(ligne["nom"], ligne["source"], ligne["reference"]))
    return trouvees
