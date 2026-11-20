"""Tous les réglages de l'analyseur halal. Change les nombres ici, pas dans le code."""

# --- Les normes testées -------------------------------------------------------
# Pour chaque norme : seuils maximum (en fraction : 0.30 = 30 %) et ce à quoi on compare.
#   base = "capitalisation"          -> valeur en bourse aujourd'hui
#   base = "capitalisation_36_mois"  -> valeur en bourse moyenne sur 36 mois
#   base = "actifs"                  -> total du bilan
# None = ce test n'existe pas dans la norme.
NORMES = {
    "stricte": {
        "nom": "Stricte (aucun intérêt)",
        "base": "capitalisation",
        "dette_max": 0.0,
        "tresorerie_max": None,
        "interets_max": 0.0,
    },
    "aaoifi": {
        "nom": "AAOIFI (norme 21)",
        "base": "capitalisation",
        "dette_max": 0.30,
        "tresorerie_max": 0.30,
        "interets_max": 0.05,
    },
    "sp": {
        "nom": "S&P Shariah",
        "base": "capitalisation_36_mois",
        "dette_max": 0.33,
        "tresorerie_max": 0.33,
        "interets_max": 0.05,
    },
    "msci": {
        "nom": "MSCI Islamic",
        "base": "actifs",
        "dette_max": 0.3333,
        "tresorerie_max": 0.3333,
        "interets_max": 0.05,
    },
    "malaisie": {
        "nom": "Malaisie (Securities Commission)",
        "base": "actifs",
        "dette_max": 0.33,
        "tresorerie_max": 0.33,
        "interets_max": 0.05,
    },
}

# La norme qui représente l'avis majoritaire (niveau « Conforme »).
NORME_MAJORITAIRE = "aaoifi"
# La norme qui représente l'avis le plus strict (niveau « unanimité »).
NORME_STRICTE = "stricte"

# --- Secteurs interdits ---------------------------------------------------------
# Mots cherchés dans le secteur et l'activité donnés par Yahoo Finance (en anglais).
SECTEURS_INTERDITS = [
    "bank", "insurance", "credit services", "mortgage", "capital markets",
    "asset management", "financial conglomerates", "brewers", "wineries",
    "distilleries", "tobacco", "gambling", "casinos", "aerospace & defense",
    "reit", "adult",
]

# Entreprises dont l'activité interdite n'apparaît pas toujours dans leur secteur Yahoo.
# Morceau du nom de l'entreprise (en minuscules, sans accents) -> raison.
# On cherche par le nom pour reconnaître l'entreprise sur toutes les bourses
# (LVMH à Paris, à New York, à Francfort…). Liste à compléter.
ACTIVITES_INTERDITES_CONNUES = {
    "moet hennessy": "vins et spiritueux (Moët, Hennessy) : plus de 5 % du chiffre d'affaires",
    "pernod ricard": "spiritueux",
    "remy cointreau": "spiritueux",
    "diageo": "spiritueux",
    "heineken": "bière",
    "anheuser-busch": "bière",
    "carlsberg": "bière",
    "constellation brands": "vins et bières",
    "philip morris": "tabac",
    "british american tobacco": "tabac",
}

# --- Recherche ------------------------------------------------------------------
NB_PROPOSITIONS = 5           # nombre d'actions proposées quand on cherche un nom
SIMILARITE_MIN = 0.6          # 0 à 1 : à partir de quand un nom connu « ressemble »
