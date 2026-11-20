"""Analyseur halal : tape le nom d'une action, le programme dit à quel point elle est conforme.

Utilisation :  python analyser.py "apple"
"""
import sys

from agentbourse import alertes, conformite, donnees, etf, recherche

LEGENDE = """
=====================================================================
 COMMENT LIRE LE RÉSULTAT
=====================================================================
 Deux vérifications :
   1. NOTRE CALCUL, avec 5 normes (détail plus bas), plus un détecteur
      d'activités interdites cachées (supermarché, filiale de crédit…).
   2. L'AVIS DES FONDS ISLAMIQUES professionnels (ETF iShares MSCI
      Islamic et SP Funds S&P 500 Sharia), qui ont des données
      payantes plus complètes que les nôtres.
 RÈGLE : on ne donne JAMAIS d'avis positif à une action qu'aucun
 fonds islamique ne garde.

 Avis positifs (nos 2 vérifications sont d'accord) :
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
    (S&P Shariah, MSCI Islamic ou Malaisie). Cas limite.

 Pas d'avis positif :
 🟠 Écartée par les fonds islamiques
    Notre calcul ne trouve rien, mais les fonds islamiques l'écartent :
    ils ont vu quelque chose que nos données gratuites ne montrent pas.
 🟠 À vérifier
    Activité interdite peut-être cachée (supermarché qui vend de
    l'alcool, filiale de crédit, divertissement…).
 ⚪ Non confirmée
    Aucun des fonds islamiques suivis ne couvre cette action (petite
    entreprise, ou bourse non suivie) : impossible de confirmer.
 ⚪ Données insuffisantes
    Il manque des chiffres pour trancher.
 🔴 Non conforme
    Activité interdite (banque, alcool, jeux, tabac, armement…) ou
    échec à toutes les normes.

 Purification : part de chaque dividende à donner en aumône, car
 elle vient d'intérêts.

 ⚠️  Notre calcul utilise UNIQUEMENT des données publiques gratuites
 (Yahoo Finance), parfois fausses, anciennes ou incomplètes.
 Outil de tri, pas une fatwa. Certains savants refusent toute
 entreprise qui a la moindre dette à intérêt. En cas de doute,
 demande à une personne de savoir.
=====================================================================
"""

TITRES = {
    conformite.UNANIMITE: "✅ Conforme à l'unanimité",
    conformite.MAJORITAIRE: "🟢 Conforme (avis majoritaire)",
    conformite.MINORITAIRE: "🟡 (Conforme) avis minoritaire",
    conformite.ECARTEE: "🟠 Écartée par les fonds islamiques",
    conformite.A_VERIFIER: "🟠 À vérifier",
    conformite.NON_CONFIRMEE: "⚪ Non confirmée",
    conformite.INSUFFISANT: "⚪ Données insuffisantes",
    conformite.NON_CONFORME: "🔴 Non conforme",
}

STATUTS_FONDS = {
    "gardee": "gardée par {fonds}",
    "ecartee": "ÉCARTÉE : présente dans les indices normaux, mais aucun fonds islamique ne la garde",
    "non_couverte": "non couverte par les fonds suivis",
}


def _pourcent(valeur: float | None) -> str:
    return "inconnu" if valeur is None else f"{valeur * 100:.1f} %"


def choisir_action(texte: str) -> recherche.Proposition | None:
    propositions = recherche.chercher(texte)
    if not propositions:
        print(f"Aucune action trouvée pour « {texte} ». Essaie un autre nom ou le code (ex. AAPL).")
        return None
    print("\nTu cherches bien l'une de ces actions ?")
    for numero, p in enumerate(propositions, start=1):
        print(f"  {numero}. {p.nom} ({p.symbole}) {p.bourse}")
    choix = input("Tape son numéro (ou Entrée pour annuler) : ").strip()
    if not choix.isdigit() or not 1 <= int(choix) <= len(propositions):
        return None
    return propositions[int(choix) - 1]


def afficher(chiffres: conformite.Chiffres, fonds: etf.Fonds) -> None:
    niveau_calcule, resultats, raison = conformite.analyser(chiffres)
    liste_alertes = alertes.detecter(chiffres.activite, chiffres.description)
    avis = fonds.avis(chiffres.symbole, chiffres.nom)
    niveau = conformite.niveau_final(niveau_calcule, liste_alertes, avis.statut)

    print(f"\n{chiffres.nom} ({chiffres.symbole}) — {chiffres.pays}, {chiffres.activite}")
    print(f"\n  RÉSULTAT : {TITRES[niveau]}")
    if raison:
        print(f"  Raison : {raison}")

    print(f"\n  1. Notre calcul (données publiques gratuites) : {TITRES[niveau_calcule]}")
    for r in resultats.values():
        etat = {True: "passe", False: "échoue", None: "inconnu"}[r.conforme]
        print(f"   - {r.nom} : {etat}")
        for t in r.tests:
            signe = {True: "ok", False: "TROP", None: "?"}[t.reussi]
            print(f"       {t.libelle} : {_pourcent(t.ratio)} (max {_pourcent(t.seuil)}) {signe}")
    print("     Activités cachées : " + ("rien trouvé" if not liste_alertes else ""))
    for a in liste_alertes:
        print(f"       ⚠️  {a}")

    print("\n  2. Avis des fonds islamiques : "
          + STATUTS_FONDS[avis.statut].format(fonds=", ".join(avis.gardee_par)))

    if niveau in conformite.POSITIFS:
        print(f"\n  Purification : donner {_pourcent(conformite.purification(chiffres))} de chaque dividende.")


def main() -> None:
    print(LEGENDE)
    texte = " ".join(sys.argv[1:]) or input("Nom de l'action : ")
    action = choisir_action(texte)
    if action is None:
        return
    print(f"\nRécupération des chiffres de {action.nom} et de la composition des fonds islamiques…")
    afficher(donnees.charger(action.symbole), etf.Fonds())


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
