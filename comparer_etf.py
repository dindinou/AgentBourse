"""Compare notre analyseur aux vrais ETF islamiques.

On prend les plus grosses actions du MSCI World (l'indice « normal ») et on regarde :
  - si elles sont dans l'ETF iShares MSCI World Islamic (donc jugées conformes par MSCI),
  - pour les américaines, si elles sont dans l'ETF SP Funds S&P 500 Sharia (SPUS),
puis on compare avec ce que dit notre programme.

Fichiers lus dans donnees_etf/ (téléchargés sur les sites d'iShares et de SP Funds) :
  swda.csv (MSCI World), iswd.csv (MSCI World Islamic), spus.csv (S&P 500 Sharia).
Résultat écrit dans docs/comparaison-etf.md.

Utilisation :  python comparer_etf.py
"""
import csv
import sys
from datetime import date
from pathlib import Path

from agentbourse import config, conformite, donnees

DOSSIER = Path(__file__).parent / "donnees_etf"

# Bourse (nom iShares) -> fin du code Yahoo.
SUFFIXES = {
    "New York Stock Exchange Inc.": "", "NASDAQ": "", "Cboe BZX formerly known as BATS": "",
    "Tokyo Stock Exchange": ".T", "Toronto Stock Exchange": ".TO", "London Stock Exchange": ".L",
    "Nyse Euronext - Euronext Paris": ".PA", "Xetra": ".DE", "Asx - All Markets": ".AX",
    "SIX Swiss Exchange": ".SW", "Euronext Amsterdam": ".AS", "Borsa Italiana": ".MI",
    "Hong Kong Exchanges And Clearing Ltd": ".HK", "Bolsa De Madrid": ".MC",
    "Singapore Exchange": ".SI", "Omx Nordic Exchange Copenhagen A/S": ".CO",
    "Nasdaq Omx Helsinki Ltd.": ".HE", "Tel Aviv Stock Exchange": ".TA", "Oslo Bors Asa": ".OL",
    "Nasdaq Omx Nordic": ".ST", "Euronext Brussels": ".BR",
}


def lire_ishares(nom_fichier: str) -> list[dict]:
    """Lit un fichier iShares (9 lignes d'en-tête avant le tableau). Ne garde que les actions."""
    with open(DOSSIER / nom_fichier, encoding="utf-8-sig") as f:
        lignes = f.read().splitlines()
    debut = next(i for i, l in enumerate(lignes) if l.startswith("Ticker,"))
    lecteur = csv.DictReader(lignes[debut:])
    return [l for l in lecteur if l.get("Asset Class") == "Equity" and l.get("Ticker")]


def symbole_yahoo(ligne: dict) -> str | None:
    suffixe = SUFFIXES.get(ligne["Exchange"])
    if suffixe is None:
        return None
    code = ligne["Ticker"].strip().rstrip(".")
    if suffixe == "":
        code = code.replace(".", "-").replace(" ", "-")
    if suffixe == ".HK":
        code = code.zfill(4)
    return code + suffixe


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    monde = lire_ishares("swda.csv")
    monde.sort(key=lambda l: float(l["Weight (%)"]), reverse=True)
    # Code + bourse : le même code peut désigner deux entreprises (SAN = Sanofi à Paris, Santander à Madrid).
    islamique_msci = {(l["Ticker"], l["Exchange"]) for l in lire_ishares("iswd.csv")}
    with open(DOSSIER / "spus.csv", encoding="utf-8-sig") as f:
        islamique_sp = {l["StockTicker"].replace(".", "-") for l in csv.DictReader(f)}

    lignes = []
    for ligne in monde[: config.COMPARAISON_NB_ACTIONS]:
        symbole = symbole_yahoo(ligne)
        if symbole is None:
            continue
        americaine = SUFFIXES[ligne["Exchange"]] == ""
        try:
            chiffres = donnees.charger(symbole)
            niveau, resultats, raison = conformite.analyser(chiffres)
        except Exception as erreur:  # action introuvable sur Yahoo, etc.
            print(f"  {symbole} : impossible ({erreur})")
            continue
        lignes.append({
            "nom": ligne["Name"].title(), "symbole": symbole, "niveau": niveau, "raison": raison or "",
            "msci_etf": (ligne["Ticker"], ligne["Exchange"]) in islamique_msci,
            "msci_nous": None if raison else resultats["msci"].conforme,
            "sp_etf": (symbole in islamique_sp) if americaine else None,
            "sp_nous": (None if raison else resultats["sp"].conforme) if americaine else None,
        })
        print(f"  {symbole:10} {niveau:12} MSCI ETF={lignes[-1]['msci_etf']}")

    ecrire_rapport(lignes)


def _accord(lignes, cle_etf, cle_nous):
    """Compte les cas où notre test MSCI (ou S&P) donne le même avis que l'ETF."""
    comparables = [l for l in lignes if l[cle_etf] is not None and (l[cle_nous] is not None or l["raison"])]
    def nous(l):  # secteur interdit = non conforme pour nous
        return False if l["raison"] else l[cle_nous]
    d_accord = [l for l in comparables if nous(l) == l[cle_etf]]
    trop_gentils = [l for l in comparables if nous(l) and not l[cle_etf]]
    trop_severes = [l for l in comparables if not nous(l) and l[cle_etf]]
    return comparables, d_accord, trop_gentils, trop_severes


def ecrire_rapport(lignes) -> None:
    oui = lambda v: "—" if v is None else ("oui" if v else "non")
    texte = [f"# Comparaison avec les ETF islamiques ({date.today():%d/%m/%Y})", "",
             f"Les {len(lignes)} plus grosses actions du MSCI World passées dans notre analyseur, "
             "comparées à la composition réelle de deux ETF islamiques :",
             "- **iShares MSCI World Islamic** (norme MSCI Islamic, monde entier) ;",
             "- **SP Funds S&P 500 Sharia (SPUS)** (norme S&P Shariah, actions américaines).", ""]
    for titre, cle_etf, cle_nous in [("MSCI Islamic", "msci_etf", "msci_nous"), ("S&P Shariah", "sp_etf", "sp_nous")]:
        comparables, d_accord, gentils, severes = _accord(lignes, cle_etf, cle_nous)
        if not comparables:
            continue
        texte += [f"## Norme {titre}", "",
                  f"- Même avis que l'ETF : **{len(d_accord)} sur {len(comparables)}** "
                  f"({len(d_accord) / len(comparables):.0%}).",
                  f"- 🚨 **Nous disons conforme, l'ETF l'écarte : {len(gentils)}** (le cas grave) : "
                  + (", ".join(f"{l['nom']} ({l['symbole']})" for l in gentils) or "aucun") + ".",
                  f"- Nous l'écartons, l'ETF la garde : {len(severes)} : "
                  + (", ".join(f"{l['nom']} ({l['symbole']})" for l in severes) or "aucun") + ".", ""]
    texte += ["## Détail", "",
              "| Action | Code | Notre niveau | Notre test MSCI | Dans l'ETF MSCI | Notre test S&P | Dans l'ETF S&P |",
              "|---|---|---|---|---|---|---|"]
    for l in lignes:
        texte.append(f"| {l['nom']} | {l['symbole']} | {l['niveau']} {l['raison']} | {oui(l['msci_nous'])} | "
                     f"{oui(l['msci_etf'])} | {oui(l['sp_nous'])} | {oui(l['sp_etf'])} |")
    (Path(__file__).parent / "docs" / "comparaison-etf.md").write_text("\n".join(texte) + "\n", encoding="utf-8")
    print("\nRapport écrit dans docs/comparaison-etf.md")


if __name__ == "__main__":
    main()
