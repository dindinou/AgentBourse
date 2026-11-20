"""Le cœur de l'analyseur : à partir des chiffres d'une entreprise, dire si elle passe chaque norme.

Aucun accès à internet ici : seulement des calculs, faciles à tester.
"""
import unicodedata
from dataclasses import dataclass, field

from agentbourse import config


@dataclass
class Chiffres:
    """Les chiffres d'une entreprise (tous dans la même devise)."""
    symbole: str
    nom: str
    secteur: str = ""
    activite: str = ""
    pays: str = ""
    devise: str = ""
    capitalisation: float | None = None          # valeur en bourse aujourd'hui
    capitalisation_36_mois: float | None = None  # valeur en bourse moyenne sur 36 mois
    actifs: float | None = None                  # total du bilan
    dette: float | None = None                   # dette totale (à intérêt)
    tresorerie: float | None = None              # trésorerie + placements financiers (court et long terme)
    revenus_interets: float | None = None
    chiffre_affaires: float | None = None


@dataclass
class Test:
    libelle: str
    ratio: float | None
    seuil: float

    @property
    def reussi(self) -> bool | None:
        return None if self.ratio is None else self.ratio <= self.seuil


@dataclass
class ResultatNorme:
    cle: str
    nom: str
    tests: list[Test] = field(default_factory=list)

    @property
    def conforme(self) -> bool | None:
        """True si tous les tests passent, False si un échoue, None s'il manque des chiffres."""
        resultats = [t.reussi for t in self.tests]
        if False in resultats:
            return False
        if None in resultats:
            return None
        return True


# Les niveaux de l'échelle, du meilleur au pire.
UNANIMITE = "unanimite"
MAJORITAIRE = "majoritaire"
MINORITAIRE = "minoritaire"
NON_CONFORME = "non_conforme"
INSUFFISANT = "insuffisant"


def _division(haut: float | None, bas: float | None) -> float | None:
    if haut is None or bas is None or bas <= 0:
        return None
    return max(haut, 0.0) / bas


def tester_norme(chiffres: Chiffres, cle: str) -> ResultatNorme:
    norme = config.NORMES[cle]
    base = getattr(chiffres, norme["base"])
    resultat = ResultatNorme(cle, norme["nom"])
    if norme["dette_max"] is not None:
        resultat.tests.append(Test("Dette", _division(chiffres.dette, base), norme["dette_max"]))
    if norme["tresorerie_max"] is not None:
        resultat.tests.append(
            Test("Trésorerie et placements", _division(chiffres.tresorerie, base), norme["tresorerie_max"])
        )
    if norme["interets_max"] is not None:
        resultat.tests.append(
            Test("Revenus d'intérêts / CA",
                 _division(chiffres.revenus_interets, chiffres.chiffre_affaires),
                 norme["interets_max"])
        )
    return resultat


def raison_secteur_interdit(chiffres: Chiffres) -> str | None:
    """Renvoie pourquoi le secteur est interdit, ou None s'il ne l'est pas (à notre connaissance)."""
    nom = unicodedata.normalize("NFKD", chiffres.nom).encode("ascii", "ignore").decode().lower()
    for morceau, raison in config.ACTIVITES_INTERDITES_CONNUES.items():
        if morceau in nom:
            return raison
    texte = f"{chiffres.secteur} {chiffres.activite}".lower()
    for mot in config.SECTEURS_INTERDITS:
        if mot in texte:
            return f"secteur interdit ({chiffres.activite or chiffres.secteur})"
    return None


def niveau(resultats: dict[str, ResultatNorme], raison_secteur: str | None) -> str:
    """Place l'action sur l'échelle de conformité."""
    if raison_secteur:
        return NON_CONFORME
    stricte = resultats[config.NORME_STRICTE].conforme
    majoritaire = resultats[config.NORME_MAJORITAIRE].conforme
    autres = [r.conforme for cle, r in resultats.items()
              if cle not in (config.NORME_STRICTE, config.NORME_MAJORITAIRE)]

    if stricte and majoritaire and all(autres):
        return UNANIMITE
    if majoritaire:
        return MAJORITAIRE
    if majoritaire is None:
        # On ne peut pas parler d'avis majoritaire sans ses chiffres.
        return NON_CONFORME if all(c is False for c in autres) and autres else INSUFFISANT
    if any(autres):
        return MINORITAIRE
    return NON_CONFORME


def purification(chiffres: Chiffres) -> float | None:
    """Part de chaque dividende à donner en aumône (revenus d'intérêts / chiffre d'affaires)."""
    return _division(chiffres.revenus_interets, chiffres.chiffre_affaires)


def analyser(chiffres: Chiffres) -> tuple[str, dict[str, ResultatNorme], str | None]:
    resultats = {cle: tester_norme(chiffres, cle) for cle in config.NORMES}
    raison = raison_secteur_interdit(chiffres)
    return niveau(resultats, raison), resultats, raison
