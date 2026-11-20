"""Analyseur halal : tape le nom d'une action, le programme dit à quel point elle est conforme.

Utilisation :  python analyser.py "apple"
"""
import sys

from agentbourse import config, conformite, donnees, recherche

LEGENDE = """
=====================================================================
 COMMENT LIRE LE RÉSULTAT
=====================================================================
 ✅ Conforme à l'unanimité
    Passe toutes les normes, y compris la plus stricte : aucune dette
    à intérêt, aucun revenu d'intérêt, activité permise.

 🟢 Conforme (avis majoritaire)
    Passe la norme de l'AAOIFI (norme n° 21). C'est l'organisme
    international de référence en finance islamique, et la plupart
    des savants contemporains acceptent ses seuils : un peu de dette
    est toléré, à condition de purifier les dividendes.

 🟡 (Conforme) avis minoritaire
    Échoue à l'AAOIFI, mais passe au moins une norme plus souple
    (S&P Shariah, MSCI Islamic ou Malaisie), qui acceptent des seuils
    un peu plus hauts ou se comparent au bilan plutôt qu'à la valeur
    en bourse. Cas limite.

 🔴 Non conforme
    Activité interdite (banque, alcool, jeux, tabac, armement…) ou
    échec à toutes les normes.

 ⚪ Données insuffisantes
    Il manque des chiffres pour trancher.

 Purification : part de chaque dividende à donner en aumône, car
 elle vient d'intérêts.

 ⚠️  IMPORTANT : chaque résultat est obtenu UNIQUEMENT avec des
 données publiques gratuites (Yahoo Finance), parfois fausses,
 anciennes ou incomplètes. Elles ne disent pas, par exemple, quelle
 part du chiffre d'affaires vient d'une activité interdite cachée.
 Un « conforme » ici veut dire « rien d'interdit trouvé dans ces
 données », pas « vérifié ». Tout reste à vérifier.

 Outil de tri, pas une fatwa. Certains savants refusent toute
 entreprise qui a la moindre dette à intérêt. En cas de doute,
 demande à une personne de savoir.
=====================================================================
"""

TITRES = {
    conformite.UNANIMITE: "✅ Conforme à l'unanimité",
    conformite.MAJORITAIRE: "🟢 Conforme (avis majoritaire)",
    conformite.MINORITAIRE: "🟡 (Conforme) avis minoritaire",
    conformite.NON_CONFORME: "🔴 Non conforme",
    conformite.INSUFFISANT: "⚪ Données insuffisantes",
}


def _pourcent(valeur: float | None) -> str:
    return "inconnu" if valeur is None else f"{valeur * 100:.1f} %"


def choisir_action(texte: str) -> recherche.Proposition | None:
    propositions = recherche.chercher(texte)
    if not propositions:
        print(f"Aucune action trouvée pour « {texte} ». Essaie un autre nom ou le code (ex. AAPL).")
        return None
    print(f"\nTu cherches bien l'une de ces actions ?")
    for numero, p in enumerate(propositions, start=1):
        print(f"  {numero}. {p.nom} ({p.symbole}) {p.bourse}")
    choix = input("Tape son numéro (ou Entrée pour annuler) : ").strip()
    if not choix.isdigit() or not 1 <= int(choix) <= len(propositions):
        return None
    return propositions[int(choix) - 1]


def afficher(chiffres: conformite.Chiffres) -> None:
    niveau, resultats, raison = conformite.analyser(chiffres)
    print(f"\n{chiffres.nom} ({chiffres.symbole}) — {chiffres.pays}, {chiffres.activite}")
    print(f"\n  RÉSULTAT : {TITRES[niveau]}")
    print("  (selon les seules données publiques gratuites : à vérifier)")
    if raison:
        print(f"  Raison : {raison}")
    print("\n  Détail par norme :")
    for r in resultats.values():
        etat = {True: "passe", False: "échoue", None: "inconnu"}[r.conforme]
        print(f"   - {r.nom} : {etat}")
        for t in r.tests:
            signe = {True: "ok", False: "TROP", None: "?"}[t.reussi]
            print(f"       {t.libelle} : {_pourcent(t.ratio)} (max {_pourcent(t.seuil)}) {signe}")
    if niveau in (conformite.MAJORITAIRE, conformite.MINORITAIRE, conformite.UNANIMITE):
        print(f"\n  Purification : donner {_pourcent(conformite.purification(chiffres))} de chaque dividende.")


def main() -> None:
    print(LEGENDE)
    texte = " ".join(sys.argv[1:]) or input("Nom de l'action : ")
    action = choisir_action(texte)
    if action is None:
        return
    print(f"\nRécupération des chiffres de {action.nom}…")
    afficher(donnees.charger(action.symbole))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
