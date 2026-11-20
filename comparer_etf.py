"""Compare notre calcul aux vrais ETF islamiques, pour mesurer nos erreurs.

On prend les plus grosses actions du MSCI World (l'indice « normal »), on les passe dans notre
calcul et notre détecteur d'activités cachées, et on regarde si les fonds islamiques les gardent.
Le cas grave : notre calcul dit « conforme » alors que les fonds l'écartent.
Résultat écrit dans docs/comparaison-etf.md.

Utilisation :  python comparer_etf.py
"""
import sys
from datetime import date
from pathlib import Path

from agentbourse import alertes, config, conformite, donnees, etf, onu


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    fonds = etf.Fonds()
    liste_onu = onu.charger()
    monde = etf.lire("swda", config.INDICES_PARENTS["swda"])  # déjà classé de la plus grosse à la plus petite

    lignes = []
    for action in [a for a in monde if a.symbole][: config.COMPARAISON_NB_ACTIONS]:
        try:
            chiffres = donnees.charger(action.symbole)
        except Exception as erreur:  # action introuvable sur Yahoo, etc.
            print(f"  {action.symbole} : impossible ({erreur})")
            continue
        niveau_calcule, _, raison = conformite.analyser(chiffres)
        liste_alertes = alertes.detecter(chiffres.activite, chiffres.description)
        avis = fonds.avis(chiffres.symbole, chiffres.nom)
        citations = onu.citations(chiffres.symbole, chiffres.nom, liste_onu)
        lignes.append({
            "nom": action.nom.title(), "symbole": action.symbole, "calcul": niveau_calcule,
            "raison": raison or "", "alertes": liste_alertes, "fonds": avis.gardee_par,
            "onu": citations,
            "final": conformite.niveau_final(niveau_calcule, liste_alertes, avis.statut, bool(citations)),
        })
        print(f"  {action.symbole:10} {niveau_calcule:12} alertes={len(liste_alertes)} fonds={len(avis.gardee_par)}")
    ecrire_rapport(lignes)


def _liste(lignes) -> str:
    return ", ".join(f"{l['nom']} ({l['symbole']})" for l in lignes) or "aucune"


def ecrire_rapport(lignes) -> None:
    positif = lambda l: l["calcul"] in conformite.POSITIFS
    gardees = [l for l in lignes if l["fonds"]]
    ecartees = [l for l in lignes if not l["fonds"]]
    graves = [l for l in ecartees if positif(l)]
    attrapees = [l for l in graves if l["alertes"]]
    ratees = [l for l in graves if not l["alertes"]]
    fausses_alertes = [l for l in gardees if l["alertes"]]
    trop_severes = [l for l in gardees if not positif(l)]
    citees = [l for l in lignes if l["onu"]]
    citees_gardees = [l for l in citees if l["fonds"]]
    texte = [
        f"# Comparaison avec les ETF islamiques ({date.today():%d/%m/%Y})", "",
        f"Les {len(lignes)} plus grosses actions du MSCI World, passées dans notre calcul, puis comparées à la "
        "composition de 4 fonds islamiques : " + ", ".join(f["nom"] for f in config.FONDS_ISLAMIQUES.values()) + ".",
        "",
        f"- Gardées par au moins un fonds islamique : **{len(gardees)}** ; écartées par tous : **{len(ecartees)}**.",
        f"- 🚨 **Cas graves** (notre calcul dit conforme, les fonds écartent) : **{len(graves)}**.",
        f"  - attrapés par notre détecteur d'activités cachées : **{len(attrapees)}** : {_liste(attrapees)}.",
        f"  - ratés par notre détecteur : **{len(ratees)}** : {_liste(ratees)}.",
        "  - Avec la règle « jamais positif sans un fonds islamique », ces cas graves ne reçoivent plus d'avis "
        "positif : ils sont affichés « 🟠 Écartée par les fonds islamiques ».",
        f"- Fausses alertes (alerte, mais un fonds islamique la garde) : {len(fausses_alertes)} : {_liste(fausses_alertes)}.",
        f"- Trop sévères (notre calcul l'écarte, un fonds la garde) : {len(trop_severes)} : {_liste(trop_severes)}.",
        f"- 🟣 Citées par l'ONU (Gaza, colonies) : **{len(citees)}** : {_liste(citees)}.",
        f"  - dont gardées par un fonds islamique (que notre règle bloque en plus) : **{len(citees_gardees)}** : "
        f"{_liste(citees_gardees)}.",
        "", "## Détail", "",
        "| Action | Code | Notre calcul | Alertes | Fonds islamiques qui la gardent | ONU | Résultat final |",
        "|---|---|---|---|---|---|---|",
    ]
    for l in lignes:
        texte.append(f"| {l['nom']} | {l['symbole']} | {l['calcul']} {l['raison']} | "
                     f"{'; '.join(l['alertes']) or '—'} | {', '.join(l['fonds']) or 'aucun'} | "
                     f"{'; '.join(c.reference for c in l['onu']) or '—'} | {l['final']} |")
    (Path(__file__).parent / "docs" / "comparaison-etf.md").write_text("\n".join(texte) + "\n", encoding="utf-8")
    print("\nRapport écrit dans docs/comparaison-etf.md")


if __name__ == "__main__":
    main()
