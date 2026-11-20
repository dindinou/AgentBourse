"""Simulation en argent fictif : compare les stratégies A et B sur l'ETF MSCI World Islamic.

Utilisation :  python simuler.py
Résultat affiché, et courbe enregistrée dans docs/simulation.png.
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # dessine dans un fichier, sans ouvrir de fenêtre
import matplotlib.pyplot as plt

from agentbourse import config, simulation

IMAGE = Path(__file__).parent / "docs" / "simulation.png"


def euros(valeur: float) -> str:
    return f"{valeur:,.0f} €".replace(",", " ")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    print("⚠️  Simulation en argent fictif sur les cours passés : aucun ordre réel, pas un conseil.\n")
    cours = simulation.charger_cours_eur()
    print(f"ETF {config.SIMULATION_SYMBOLE}, du {cours.index[0]:%d/%m/%Y} au {cours.index[-1]:%d/%m/%Y}, "
          f"{euros(config.VERSEMENT_MENSUEL_EUR)} par mois, frais {config.FRAIS_PAR_ORDRE_EUR:.2f} € par achat.\n")

    resultats = [simulation.strategie_a(cours), simulation.strategie_b(cours)]
    print(f"{'':44}{'Versé':>10}{'Frais':>9}{'Valeur':>11}{'Impôt':>9}{'Net':>11}{'Gain net':>11}  Achats")
    for r in resultats:
        print(f"{r.nom:44}{euros(r.verse):>10}{euros(r.frais):>9}{euros(r.valeur_finale):>11}"
              f"{euros(r.impot):>9}{euros(r.net_apres_impot):>11}{euros(r.gain_net):>11}  {r.nb_achats}")
    a, b = resultats
    meilleure = a if a.net_apres_impot >= b.net_apres_impot else b
    print(f"\nMeilleure sur cette période : {meilleure.nom} "
          f"(écart {euros(abs(a.net_apres_impot - b.net_apres_impot))} après impôt).")
    print("Impôt = flat tax si on vendait tout le dernier jour. Les résultats passés ne disent rien du futur.")

    fig, ax = plt.subplots(figsize=(10, 5))
    for r in resultats:
        ax.plot(r.courbe.index, r.courbe.values, label=r.nom)
    verse = (a.courbe * 0 + config.VERSEMENT_MENSUEL_EUR).where(
        a.courbe.index.isin(list(simulation.jours_de_versement(cours))), 0).cumsum()
    ax.plot(verse.index, verse.values, label="Argent versé", color="grey", linestyle="--")
    ax.set_title("Simulation en argent fictif — ETF MSCI World Islamic (en euros)")
    ax.set_ylabel("Valeur du portefeuille (€)")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(IMAGE, dpi=120)
    print(f"\nCourbe enregistrée dans {IMAGE.relative_to(Path(__file__).parent)}")


if __name__ == "__main__":
    main()
