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

# --- Activités à risque (cachées) -------------------------------------------------
# Ne rendent pas l'action « non conforme », mais empêchent de dire « conforme » : « à vérifier ».
# Activité Yahoo -> raison.
ACTIVITES_A_RISQUE = {
    "Discount Stores": "supermarché : vend souvent de l'alcool et du porc",
    "Grocery Stores": "supermarché : vend souvent de l'alcool et du porc",
    "Department Stores": "grand magasin : vend souvent de l'alcool",
    "Internet Retail": "vente en ligne : vend souvent de l'alcool et du porc",
    "Restaurants": "restauration : porc ou alcool possibles",
    "Lodging": "hôtellerie : alcool, souvent jeux",
    "Resorts & Casinos": "jeux d'argent",
    "Entertainment": "divertissement (musique, films) : exclu par les fonds islamiques",
    "Broadcasting": "médias et divertissement : exclus par les fonds islamiques",
    "Advertising Agencies": "publicité : exclue par la norme S&P",
    "Internet Content & Information": "revenus de publicité : exclus par la norme S&P",
}
# Phrase cherchée dans la description de l'entreprise (en anglais, expression régulière) -> raison.
PHRASES_A_RISQUE = {
    r"financial (products|services) segment": "filiale de crédit ou d'assurance",
    r"\b(provides?|offers?) (retail |wholesale |customer |dealer )*(financing|loans|leasing)": "filiale de crédit",
    r"\b(life|non-life|property and casualty) insurance": "activité d'assurance",
    r"\bbanking (services|business|operations)": "activité bancaire",
    r"(?<!non-)\balcoholic beverages|\b(beer|wines?|spirits|liquor)\b(?! industry)": "alcool",
    r"\btobacco\b|\bcigarettes?\b": "tabac",
    r"\bpork\b|\bham\b|\bbacon\b": "porc",
    r"\b(casinos?|gambling|lotter(y|ies)|betting)\b": "jeux d'argent",
    r"\b(music|motion pictures?|film) (segment|production|distribution|entertainment)": "divertissement",
    r"\b(weapons|munitions|missiles|firearms)\b": "armement",
}

# --- Recherche ------------------------------------------------------------------
NB_PROPOSITIONS = 5           # nombre d'actions proposées quand on cherche un nom
SIMILARITE_MIN = 0.6          # 0 à 1 : à partir de quand un nom connu « ressemble »

# --- Avis des ETF islamiques (deuxième vérification) -----------------------------
# Composition téléchargée sur les sites des fonds, gardée dans donnees_etf/.
_ISHARES = "https://www.ishares.com/ch/individual/en/products/{id}/x/1495092304805.ajax?fileType=csv&fileName=X_holdings&dataType=fund"
FONDS_ISLAMIQUES = {
    "iswd": {"nom": "iShares MSCI World Islamic", "url": _ISHARES.format(id=251394), "format": "ishares"},
    "isus": {"nom": "iShares MSCI USA Islamic", "url": _ISHARES.format(id=251393), "format": "ishares"},
    "isde": {"nom": "iShares MSCI EM Islamic", "url": _ISHARES.format(id=251392), "format": "ishares"},
    "spus": {"nom": "SP Funds S&P 500 Sharia",
             "url": "https://www.sp-funds.com/wp-content/uploads/data/TidalFG_Holdings_SPUS.csv", "format": "spfunds"},
}
# Indices « normaux » : une action qui y est mais qu'aucun fonds islamique ne garde a été écartée.
INDICES_PARENTS = {
    "swda": {"nom": "iShares Core MSCI World", "url": _ISHARES.format(id=251882), "format": "ishares"},
    "eimi": {"nom": "iShares Core MSCI EM IMI", "url": _ISHARES.format(id=264659), "format": "ishares"},
}
ETF_RAFRAICHIR_APRES_JOURS = 7   # on retélécharge les compositions plus vieilles que ça

# --- Comparaison avec les ETF islamiques ------------------------------------------
# Nombre de plus grosses actions du MSCI World analysées (plus = plus long).
COMPARAISON_NB_ACTIONS = 150

# --- Simulation en argent fictif (partie 2) ------------------------------------------
SIMULATION_SYMBOLE = "ISDW.L"        # iShares MSCI World Islamic (IE00B27YCN58), cotée en dollars à Londres
SIMULATION_DEVISE = "USD"            # devise de cotation, convertie en euros
SIMULATION_DEBUT = "2015-01-01"
VERSEMENT_MENSUEL_EUR = 70.0
FRAIS_PAR_ORDRE_EUR = 1.0            # frais fixes du courtier à chaque achat (0 si plan d'épargne gratuit)
FRAIS_PAR_ORDRE_POURCENT = 0.0       # frais en pourcentage de chaque achat (0.001 = 0,1 %)
MOYENNE_JOURS = 200                  # stratégie B : on achète quand le cours passe sous sa moyenne sur ce nombre de jours
FLAT_TAX = 0.314                     # impôt français sur les plus-values (prélèvement forfaitaire unique)
