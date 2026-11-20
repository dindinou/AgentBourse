"""Simulation en argent fictif : que serait devenu un versement de 70 €/mois depuis 2015 ?

Stratégie A : on achète chaque mois, quoi qu'il arrive.
Stratégie B : « acheter au bon moment » : on met l'argent de côté, et on achète tout
              dès que le cours passe sous sa moyenne des 200 derniers jours.

Aucun vrai ordre n'est passé : ce ne sont que des calculs sur les cours passés.
"""
from dataclasses import dataclass

import pandas as pd

from agentbourse import config


@dataclass
class Resultat:
    nom: str
    verse: float               # total de l'argent mis de côté
    frais: float               # total des frais payés
    valeur_finale: float       # parts au dernier cours + argent pas encore investi
    impot: float               # flat tax si on vendait tout à la fin
    nb_achats: int
    courbe: pd.Series          # valeur du portefeuille chaque jour

    @property
    def net_apres_impot(self) -> float:
        return self.valeur_finale - self.impot

    @property
    def gain_net(self) -> float:
        return self.net_apres_impot - self.verse


def frais(montant: float) -> float:
    return config.FRAIS_PAR_ORDRE_EUR + montant * config.FRAIS_PAR_ORDRE_POURCENT


def jours_de_versement(cours: pd.Series) -> set:
    """Le premier jour de bourse de chaque mois."""
    mois = cours.index.to_period("M")
    return set(cours.index[~mois.duplicated()])


def simuler(cours: pd.Series, nom: str, acheter_maintenant) -> Resultat:
    """Moteur commun. acheter_maintenant(jour) dit si on investit l'argent de côté ce jour-là."""
    versements = jours_de_versement(cours)
    parts = liquide = verse = total_frais = cout_achat = 0.0
    nb_achats = 0
    valeurs = []
    for jour, prix in cours.items():
        if jour in versements:
            liquide += config.VERSEMENT_MENSUEL_EUR
            verse += config.VERSEMENT_MENSUEL_EUR
        if liquide > 0 and acheter_maintenant(jour):
            f = frais(liquide)
            if liquide > f:  # on n'achète pas si les frais mangent tout
                parts += (liquide - f) / prix
                total_frais += f
                cout_achat += liquide  # ce qu'on a payé, frais compris (déductibles de la plus-value)
                liquide = 0.0
                nb_achats += 1
        valeurs.append(parts * prix + liquide)

    valeur_parts = parts * cours.iloc[-1]
    plus_value = max(valeur_parts - cout_achat, 0.0)
    return Resultat(nom, verse, total_frais, valeur_parts + liquide, plus_value * config.FLAT_TAX,
                    nb_achats, pd.Series(valeurs, index=cours.index))


def strategie_a(cours: pd.Series) -> Resultat:
    versements = jours_de_versement(cours)
    return simuler(cours, "A : 70 € chaque mois", lambda jour: jour in versements)


def strategie_b(cours: pd.Series) -> Resultat:
    moyenne = cours.rolling(config.MOYENNE_JOURS).mean()
    sous_la_moyenne = cours < moyenne  # faux tant que la moyenne n'existe pas (200 premiers jours)
    return simuler(cours, f"B : acheter sous la moyenne {config.MOYENNE_JOURS} jours",
                   lambda jour: bool(sous_la_moyenne[jour]))


def charger_cours_eur() -> pd.Series:
    """Cours de l'ETF en euros, dividendes réinvestis (besoin d'internet)."""
    import yfinance as yf

    debut = config.SIMULATION_DEBUT
    # auto_adjust : cours corrigé comme si les dividendes étaient réinvestis.
    etf = yf.Ticker(config.SIMULATION_SYMBOLE).history(start=debut, auto_adjust=True)["Close"]
    change = yf.Ticker(f"EUR{config.SIMULATION_DEVISE}=X").history(start=debut)["Close"]  # dollars pour 1 €
    etf.index, change.index = etf.index.tz_localize(None).normalize(), change.index.tz_localize(None).normalize()
    change = change.reindex(etf.index).ffill().bfill()
    return (etf / change).dropna()
