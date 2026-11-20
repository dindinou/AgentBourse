"""Tests de la simulation, sur des cours inventés (sans internet)."""
import pandas as pd
import pytest

from agentbourse import config, simulation as s


@pytest.fixture(autouse=True)
def reglages_simples(monkeypatch):
    monkeypatch.setattr(config, "VERSEMENT_MENSUEL_EUR", 100.0)
    monkeypatch.setattr(config, "FRAIS_PAR_ORDRE_EUR", 0.0)
    monkeypatch.setattr(config, "FRAIS_PAR_ORDRE_POURCENT", 0.0)
    monkeypatch.setattr(config, "FLAT_TAX", 0.30)
    monkeypatch.setattr(config, "MOYENNE_JOURS", 3)


def cours(valeurs, debut="2020-01-01", frequence="MS"):
    return pd.Series(valeurs, index=pd.date_range(debut, periods=len(valeurs), freq=frequence), dtype=float)


def test_prix_fixe_on_recupere_sa_mise_sans_impot():
    r = s.strategie_a(cours([10, 10, 10]))
    assert r.verse == 300 and r.valeur_finale == pytest.approx(300) and r.impot == 0 and r.nb_achats == 3


def test_prix_qui_double_impot_sur_le_gain_seulement():
    r = s.strategie_a(cours([10, 20]))  # 10 parts + 5 parts = 15 parts à 20 € = 300 €
    assert r.valeur_finale == pytest.approx(300)
    assert r.impot == pytest.approx((300 - 200) * 0.30)
    assert r.gain_net == pytest.approx(70)


def test_frais_fixes_par_achat(monkeypatch):
    monkeypatch.setattr(config, "FRAIS_PAR_ORDRE_EUR", 1.0)
    r = s.strategie_a(cours([10, 10]))
    assert r.frais == 2 and r.valeur_finale == pytest.approx(198)


def test_strategie_b_attend_que_le_cours_passe_sous_la_moyenne():
    # Moyenne sur 3 mois : le cours ne passe dessous qu'au 5e mois (8 < moyenne de 12, 12, 8).
    r = s.strategie_b(cours([10, 11, 12, 12, 8, 9]))
    assert r.nb_achats == 2       # mois 5 (tout l'argent de côté) puis mois 6 (9 < moyenne)
    assert r.verse == 600


def test_strategie_b_garde_l_argent_si_le_cours_monte_toujours():
    r = s.strategie_b(cours([10, 11, 12, 13, 14]))
    assert r.nb_achats == 0 and r.valeur_finale == 500 and r.impot == 0
