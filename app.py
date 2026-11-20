"""Tableau de bord AgentBourse : un onglet analyseur halal, un onglet simulation en argent fictif.

Lancer :  .venv/Scripts/streamlit run app.py
"""
from datetime import date

import pandas as pd
import streamlit as st

from agentbourse import alertes, config, conformite, donnees, etf, indice, onu, panier, recherche, simulation
from analyser import LEGENDE, STATUTS_FONDS, TITRES

st.set_page_config(page_title="AgentBourse", page_icon="📈", layout="wide")
st.title("AgentBourse")
st.caption("Projet d'apprentissage. Argent fictif uniquement. Ce n'est ni un conseil en investissement, ni une fatwa.")


# --- Données gardées en mémoire (pour ne pas tout retélécharger à chaque clic) -----------------
@st.cache_resource(show_spinner="Chargement de la composition des fonds islamiques…")
def fonds_islamiques() -> etf.Fonds:
    return etf.Fonds()


@st.cache_data(ttl=86400, show_spinner="Récupération des chiffres de l'entreprise…")
def chiffres_de(symbole: str) -> conformite.Chiffres:
    return donnees.charger(symbole)


@st.cache_data(ttl=3600, show_spinner=False)
def propositions(texte: str) -> list[recherche.Proposition]:
    return recherche.chercher(texte)


@st.cache_data(ttl=86400, show_spinner="Récupération des cours de l'ETF…")
def cours_etf() -> pd.Series:
    return simulation.charger_cours_eur()


@st.cache_data(ttl=86400, show_spinner="Récupération des cours des 50 actions du panier…")
def donnees_panier():
    actions = panier.composer()
    return actions, panier.rendements_eur(actions)


def pourcent(valeur: float | None) -> str:
    return "inconnu" if valeur is None else f"{valeur * 100:.1f} %"


def euros(valeur: float) -> str:
    return f"{valeur:,.0f} €".replace(",", " ")


onglet_indice, onglet_analyse, onglet_simulation, onglet_panier = st.tabs(
    ["📊 Indice AgentBourse", "🔎 Analyseur halal", "📈 Simulation en argent fictif", "🧺 Panier filtré"])

# --- Onglet 1 : analyseur ---------------------------------------------------------------------
with onglet_analyse:
    with st.expander("Comment lire le résultat (légende)"):
        st.text(LEGENDE)

    texte = st.text_input("Nom de l'action (même mal écrit)", placeholder="ex. aple, total energie, aramco")
    if texte:
        choix = propositions(texte)
        if not choix:
            st.warning(f"Aucune action trouvée pour « {texte} ». Essaie un autre nom ou le code (ex. AAPL).")
        else:
            action = st.radio("Tu cherches bien l'une de ces actions ?", choix,
                              format_func=lambda p: f"{p.nom} ({p.symbole}) {p.bourse}")
            if st.button("Analyser", type="primary"):
                chiffres = chiffres_de(action.symbole)
                niveau_calcule, resultats, raison = conformite.analyser(chiffres)
                liste_alertes = alertes.detecter(chiffres.activite, chiffres.description)
                avis = fonds_islamiques().avis(chiffres.symbole, chiffres.nom)
                citations = onu.citations(chiffres.symbole, chiffres.nom)
                niveau = conformite.niveau_final(niveau_calcule, liste_alertes, avis.statut, bool(citations))

                st.subheader(f"{chiffres.nom} ({chiffres.symbole})")
                st.caption(f"{chiffres.pays} — {chiffres.activite}")
                st.markdown(f"## {TITRES[niveau]}")
                if raison:
                    st.write(f"Raison : {raison}")
                if niveau in conformite.POSITIFS:
                    st.info(f"Purification : donner {pourcent(conformite.purification(chiffres))} de chaque dividende.")

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown("**1. Notre calcul** (données publiques gratuites)")
                    st.write(TITRES[niveau_calcule])
                    tableau = [{"Norme": r.nom, "Test": t.libelle, "Valeur": pourcent(t.ratio),
                                "Maximum": pourcent(t.seuil),
                                "Résultat": {True: "✅", False: "❌", None: "?"}[t.reussi]}
                               for r in resultats.values() for t in r.tests]
                    st.dataframe(pd.DataFrame(tableau), hide_index=True)
                    st.markdown("**Activités cachées**")
                    if liste_alertes:
                        for a in liste_alertes:
                            st.warning(a)
                    else:
                        st.write("Rien trouvé.")
                with col2:
                    st.markdown("**2. Avis des fonds islamiques**")
                    st.write(STATUTS_FONDS[avis.statut].format(fonds=", ".join(avis.gardee_par)))
                with col3:
                    st.markdown("**3. Listes de l'ONU**")
                    if citations:
                        for c in citations:
                            st.error(f"🟣 {c.source} — {c.reference}")
                    else:
                        st.write("Pas citée.")

# --- Onglet 2 : simulation --------------------------------------------------------------------
with onglet_simulation:
    st.write("Que serait devenu un versement mensuel dans l'ETF **iShares MSCI World Islamic**, "
             "converti en euros, dividendes réinvestis ? Aucun ordre réel : seulement des calculs sur les cours passés.")
    cours = cours_etf()

    g, d = st.columns(2)
    with g:
        config.VERSEMENT_MENSUEL_EUR = st.slider("Versement par mois (€)", 10, 1000, int(config.VERSEMENT_MENSUEL_EUR), 10)
        config.FRAIS_PAR_ORDRE_EUR = st.slider("Frais par achat (€)", 0.0, 5.0, float(config.FRAIS_PAR_ORDRE_EUR), 0.5)
    with d:
        config.MOYENNE_JOURS = st.slider("Stratégie B : moyenne sur combien de jours", 20, 300, int(config.MOYENNE_JOURS), 10)
        premier_jour = cours.index[0].date()  # premier jour de bourse (le 1er janvier est férié)
        debut = st.date_input("Début", max(date.fromisoformat(config.SIMULATION_DEBUT), premier_jour),
                              min_value=premier_jour, max_value=cours.index[-1].date())
    periode = cours[cours.index >= pd.Timestamp(debut)]

    resultats = [simulation.strategie_a(periode), simulation.strategie_b(periode)]
    st.dataframe(pd.DataFrame([{
        "Stratégie": r.nom, "Versé": euros(r.verse), "Frais": euros(r.frais), "Valeur": euros(r.valeur_finale),
        "Impôt (flat tax)": euros(r.impot), "Net après impôt": euros(r.net_apres_impot),
        "Gain net": euros(r.gain_net), "Achats": r.nb_achats,
    } for r in resultats]), hide_index=True)

    courbes = pd.DataFrame({r.nom: r.courbe for r in resultats})
    st.line_chart(courbes, y_label="Valeur du portefeuille (€)")
    st.caption(f"Impôt = flat tax de {config.FLAT_TAX * 100:.1f} % si on vendait tout le dernier jour. "
               "Les dividendes sont supposés réinvestis et imposés à la fin (un peu trop optimiste). "
               "Les résultats passés ne disent rien du futur.")

# --- Onglet 3 : panier filtré -----------------------------------------------------------------
with onglet_panier:
    st.write(f"Les {config.PANIER_NB_ACTIONS} plus grosses actions de l'ETF **iShares MSCI World Islamic**, "
             "comparées au même panier **sans les actions citées par l'ONU** (Gaza, colonies). "
             f"{euros(config.VERSEMENT_MENSUEL_EUR)} par mois (réglable dans l'onglet simulation), stratégie A.")
    st.warning("Composition d'aujourd'hui appliquée depuis 2015 : les deux paniers sont avantagés "
               "(on choisit après coup les entreprises qui ont réussi). Seul l'écart entre les deux a du sens.")
    actions, rendements = donnees_panier()
    retirees = [a for a in actions if a.citations]
    st.markdown("**Retirées du panier filtré :** " + "; ".join(
        f"{a.nom} ({a.poids:.1f} % du fonds) — {a.citations[0].reference}" for a in retirees))

    resultats = []
    for nom, cours_panier in panier.deux_paniers(actions, rendements).items():
        r = simulation.strategie_a(cours_panier.iloc[1:])
        r.nom = nom
        resultats.append(r)
    st.dataframe(pd.DataFrame([{
        "Panier": r.nom, "Versé": euros(r.verse), "Net après impôt": euros(r.net_apres_impot),
        "Gain net": euros(r.gain_net)} for r in resultats]), hide_index=True)
    st.line_chart(pd.DataFrame({r.nom: r.courbe for r in resultats}), y_label="Valeur du portefeuille (€)")

# --- Onglet 0 : indice AgentBourse ---------------------------------------------------------------
with onglet_indice:
    st.write("Nos règles transformées en indice : actions des fonds islamiques iShares (monde et émergents) "
             "notées **✅ unanimité** ou **🟢 avis majoritaire**, jamais citées par l'ONU, sans activité cachée détectée. "
             f"Poids selon la taille, plafonnés à {config.INDICE_PLAFOND:.0%}. Recomposé chaque trimestre, "
             "surveillé chaque soir par un agent automatique. **Argent fictif uniquement.**")
    if not indice.HISTORIQUE.exists():
        st.info("L'indice n'a pas encore été lancé.")
    else:
        historique = pd.read_csv(indice.HISTORIQUE, parse_dates=["date"]).set_index("date")
        etat = indice.lire_etat()
        dernier = historique.iloc[-1]
        c1, c2, c3 = st.columns(3)
        c1.metric("Portefeuille fictif", euros(dernier["portefeuille_eur"]),
                  f"{dernier['portefeuille_eur'] / config.INDICE_CAPITAL_DEPART_EUR - 1:+.2%} depuis le lancement")
        c2.metric("Indice (base 100)", f"{dernier['indice_base_100']:.2f}")
        c3.metric("Actions", int(dernier["nb_actions"]))
        st.caption(f"Lancé le {etat['lancement']} avec {euros(config.INDICE_CAPITAL_DEPART_EUR)} fictifs ; "
                   f"dernier cours : {etat['date']}.")
        if len(historique) > 1:
            st.line_chart(historique["portefeuille_eur"], y_label="Portefeuille fictif (€)")
        composition = pd.DataFrame([{"Action": l.nom, "Code": l.symbole, "Poids": f"{l.poids:.2%}",
                                     "Niveau": TITRES[l.niveau]} for l in indice.lire_composition()])
        st.markdown("**Composition**")
        st.dataframe(composition, hide_index=True, height=300)
        with st.expander("Journal de l'agent"):
            st.markdown(indice.JOURNAL.read_text(encoding="utf-8"))
