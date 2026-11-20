"""L'agent du soir : met à jour l'indice AgentBourse et son portefeuille fictif.

Chaque soir de bourse (automatiquement sur GitHub Actions) :
  1. fait évoluer le portefeuille avec les cours du jour (en euros, dividendes réinvestis) ;
  2. au premier passage de chaque trimestre : réanalyse ~800 actions et recompose l'indice ;
     les autres jours : surveille la conformité (citation de l'ONU, sortie des fonds islamiques) ;
  3. écrit les résultats dans indice/ (composition, historique, journal).

Argent fictif uniquement : aucun ordre réel n'est jamais passé.

Utilisation :  python agent_quotidien.py            (travail normal du soir)
               python agent_quotidien.py --reajuster (force la recomposition complète)
"""
import sys
from datetime import date

from agentbourse import config, etf, indice, onu


def trimestre(jour: str) -> str:
    annee, mois = jour[:4], int(jour[5:7])
    return f"{annee}-T{(mois - 1) // 3 + 1}"


def euros(v: float) -> str:
    return f"{v:,.2f} €".replace(",", " ")


def main(forcer: bool = False) -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    aujourd_hui = date.today().isoformat()
    etat = indice.lire_etat()
    composition = indice.lire_composition()
    journal: list[str] = []

    # 1. Évolution avec les cours du jour
    nouveaux_cours = False
    if etat and composition:
        variations, dernier = indice.variations_eur(composition, etat["date"])
        if dernier > etat["date"]:
            etat["portefeuille"] = indice.faire_evoluer(etat["portefeuille"], variations)
            etat["indice"] = indice.faire_evoluer(etat["indice"], variations)
            etat["date"] = dernier
            nouveaux_cours = True
            manquants = len(composition) - len(variations)
            if manquants:
                journal.append(f"{manquants} action(s) sans cours aujourd'hui : valeur inchangée pour elles.")

    # 2. Recomposition trimestrielle, ou surveillance
    fonds = etf.Fonds()
    liste_onu = onu.charger()
    reajuster = forcer or not etat or trimestre(aujourd_hui) != trimestre(etat["reajustement"])
    changement = False
    if reajuster:
        anciens = {l.symbole for l in composition}
        composition, bilan = indice.selectionner(fonds, liste_onu)
        nouveaux = {l.symbole for l in composition}
        journal.append(f"**Recomposition trimestrielle** : {sum(bilan.values())} actions analysées, "
                       f"**{len(composition)} retenues**. Détail des résultats : "
                       + ", ".join(f"{n} {k}" for k, n in sorted(bilan.items(), key=lambda x: -x[1])) + ".")
        if anciens:
            if nouveaux - anciens:
                journal.append("Entrées : " + ", ".join(sorted(nouveaux - anciens)) + ".")
            if anciens - nouveaux:
                journal.append("Sorties : " + ", ".join(sorted(anciens - nouveaux)) + ".")
        changement = True
    else:
        exclues = []
        for l in composition:
            citations = onu.citations(l.symbole, l.nom, liste_onu)
            if citations:
                exclues.append((l, f"citée par l'ONU ({citations[0].source} — {citations[0].reference})"))
            elif fonds.avis(l.symbole, l.nom).statut != "gardee":
                exclues.append((l, "plus aucun fonds islamique ne la garde"))
        for l, raison in exclues:
            journal.append(f"**Sortie immédiate** de {l.nom} ({l.symbole}) : {raison}.")
        if exclues:
            sortants = {l.symbole for l, _ in exclues}
            composition = indice.appliquer_poids([l for l in composition if l.symbole not in sortants])
            changement = True

    if not composition:
        print("Aucune action retenue : rien à faire.")
        return

    # 3. Achats et ventes fictifs pour revenir aux poids cibles
    if changement:
        poids = {l.symbole: l.poids for l in composition}
        if not etat:
            capital = config.INDICE_CAPITAL_DEPART_EUR
            frais = capital * config.INDICE_FRAIS_POURCENT
            etat = {"date": aujourd_hui, "lancement": aujourd_hui,
                    "portefeuille": {s: (capital - frais) * p for s, p in poids.items()},
                    "indice": {s: 100 * p for s, p in poids.items()}}
            journal.insert(0, f"**Lancement** : {euros(capital)} fictifs investis dans {len(poids)} actions "
                              f"(frais {euros(frais)}).")
        else:
            etat["portefeuille"], frais = indice.reequilibrer(etat["portefeuille"], poids, config.INDICE_FRAIS_POURCENT)
            etat["indice"], _ = indice.reequilibrer(etat["indice"], poids, 0)
            journal.append(f"Achats et ventes fictifs pour revenir aux poids cibles : frais {euros(frais)}.")
        if reajuster:
            etat["reajustement"] = aujourd_hui
        indice.ecrire_composition(composition)

    if not (nouveaux_cours or changement):
        print("Pas de nouveau cours depuis le dernier passage : rien à faire.")
        return

    valeur = sum(etat["portefeuille"].values())
    valeur_indice = sum(etat["indice"].values())
    indice.ajouter_historique(etat["date"], valeur, valeur_indice, len(composition))
    journal.append(f"Portefeuille fictif : **{euros(valeur)}** ; indice : {valeur_indice:.2f} (base 100 au lancement).")
    indice.ecrire_etat(etat)
    indice.ecrire_journal(etat["date"], journal)
    print("\n".join(journal))


if __name__ == "__main__":
    main(forcer="--reajuster" in sys.argv)
