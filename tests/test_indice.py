"""Tests de l'indice, sans internet."""
import pytest

from agentbourse import indice
from agent_quotidien import trimestre


def test_poids_proportionnels_sans_plafond_atteint():
    p = indice.poids_plafonnes({"A": 1, "B": 1, "C": 2}, plafond=0.6)
    assert p == pytest.approx({"A": 0.25, "B": 0.25, "C": 0.5})


def test_plafond_de_5_pourcent_respecte_et_somme_100():
    tailles = {"GEANT": 1000} | {f"P{i}": 10 for i in range(30)}
    p = indice.poids_plafonnes(tailles, plafond=0.05)
    assert sum(p.values()) == pytest.approx(1)
    assert max(p.values()) <= 0.05 + 1e-9
    assert p["GEANT"] == pytest.approx(0.05)


def test_trop_peu_d_actions_parts_egales():
    p = indice.poids_plafonnes({"A": 5, "B": 1}, plafond=0.05)
    assert p == {"A": 0.5, "B": 0.5}


def test_reequilibrer_vend_l_action_sortie_et_paie_les_frais():
    positions = {"A": 600.0, "B": 400.0}
    nouvelles, frais = indice.reequilibrer(positions, {"A": 1.0}, frais=0.01)
    # on vend 400 de B et on achète 400 de A : 800 échangés, 1 % de frais
    assert frais == pytest.approx(8)
    assert nouvelles == pytest.approx({"A": 992})


def test_faire_evoluer():
    assert indice.faire_evoluer({"A": 100.0, "B": 50.0}, {"A": 1.1}) == pytest.approx({"A": 110, "B": 50})


def test_trimestre():
    assert trimestre("2026-11-20") == "2026-T4"
    assert trimestre("2027-01-02") == "2027-T1"
