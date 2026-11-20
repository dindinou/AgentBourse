"""Simulation en argent fictif avec notre propre panier : le fonds islamique, moins les actions citées par l'ONU.

Utilisation :  python simuler_panier.py
Résultat affiché, et courbe enregistrée dans docs/panier.png.
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from agentbourse import config, panier, simulation
from simuler import euros

IMAGE = Path(__file__).parent / "docs" / "panier.png"


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    print("⚠️  Simulation en argent fictif sur les cours passés : aucun ordre réel, pas un conseil.")
    print("⚠️  Composition d'aujourd'hui appliquée depuis 2015 : les deux paniers sont avantagés.")
    print("    Seul l'ÉCART entre les deux a du sens.\n")

    actions = panier.composer()
    retirees = [a for a in actions if a.citations]
    print(f"{len(actions)} plus grosses actions de l'ETF MSCI World Islamic. Retirées (citées par l'ONU) :")
    for a in retirees:
        print(f"  - {a.nom} ({a.symbole}, {a.poids:.1f} % du fonds) : {a.citations[0].reference}")

    rendements = panier.rendements_eur(actions)
    manquantes = [a.symbole for a in actions if a.symbole not in rendements.columns]
    if manquantes:
        print(f"  (cours introuvables sur Yahoo, ignorées : {', '.join(manquantes)})")

    print(f"\n{config.VERSEMENT_MENSUEL_EUR:.0f} € par mois, stratégie A (chaque mois), "
          f"frais {config.FRAIS_PAR_ORDRE_EUR:.2f} € par achat :\n")
    resultats = []
    for nom, cours in panier.deux_paniers(actions, rendements).items():
        r = simulation.strategie_a(cours.iloc[1:])
        r.nom = nom
        resultats.append(r)
        print(f"  {nom:58} versé {euros(r.verse)}, net après impôt {euros(r.net_apres_impot)} "
              f"(gain {euros(r.gain_net)})")
    complet, filtre = resultats
    ecart = filtre.net_apres_impot - complet.net_apres_impot
    print(f"\nÉcart en retirant les actions citées par l'ONU : {'+' if ecart >= 0 else ''}{euros(ecart)}.")

    fig, ax = plt.subplots(figsize=(10, 5))
    for r in resultats:
        ax.plot(r.courbe.index, r.courbe.values, label=r.nom)
    ax.set_title("Simulation en argent fictif — panier complet contre panier filtré (en euros)")
    ax.set_ylabel("Valeur du portefeuille (€)")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.text(0.01, 0.01, "Composition d'aujourd'hui appliquée depuis 2015 : seul l'écart entre les courbes a du sens.",
             fontsize=8, color="grey")
    fig.tight_layout()
    fig.savefig(IMAGE, dpi=120)
    print(f"Courbe enregistrée dans {IMAGE.relative_to(Path(__file__).parent)}")


if __name__ == "__main__":
    main()
