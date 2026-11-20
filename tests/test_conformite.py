"""Tests sans internet, sur des entreprises inventées."""
from agentbourse import conformite as c
from agentbourse.recherche import depuis_liste_connue


def entreprise(**chiffres) -> c.Chiffres:
    base = dict(symbole="TEST", nom="Test", activite="Software", capitalisation=1000,
                capitalisation_36_mois=1000, actifs=1000, dette=0, tresorerie=100,
                revenus_interets=0, chiffre_affaires=1000)
    base.update(chiffres)
    return c.Chiffres(**base)


def test_aucune_dette_ni_interet_donne_unanimite():
    assert c.analyser(entreprise())[0] == c.UNANIMITE


def test_un_peu_de_dette_donne_avis_majoritaire():
    assert c.analyser(entreprise(dette=200, revenus_interets=10))[0] == c.MAJORITAIRE


def test_dette_entre_30_et_33_pourcent_donne_avis_minoritaire():
    # 31 % de la valeur en bourse : trop pour l'AAOIFI (30 %), assez pour S&P (33 %).
    assert c.analyser(entreprise(dette=310))[0] == c.MINORITAIRE


def test_dette_forte_en_bourse_mais_faible_au_bilan_donne_minoritaire():
    # MSCI et la Malaisie comparent au bilan, qui est ici bien plus gros.
    assert c.analyser(entreprise(dette=500, actifs=5000))[0] == c.MINORITAIRE


def test_trop_de_dette_partout_donne_non_conforme():
    assert c.analyser(entreprise(dette=900))[0] == c.NON_CONFORME


def test_trop_de_revenus_d_interets_donne_non_conforme():
    assert c.analyser(entreprise(revenus_interets=60))[0] == c.NON_CONFORME


def test_banque_non_conforme_meme_sans_dette():
    niveau, _, raison = c.analyser(entreprise(activite="Banks - Regional"))
    assert niveau == c.NON_CONFORME and "interdit" in raison


def test_activite_interdite_connue_sur_toutes_les_bourses():
    for symbole in ("MC.PA", "LVMUY", "MOH.DE"):
        lvmh = entreprise(symbole=symbole, activite="Luxury Goods",
                          nom="LVMH Moët Hennessy - Louis Vuitton, Société Européenne")
        assert c.analyser(lvmh)[0] == c.NON_CONFORME


def test_chiffres_manquants_donne_insuffisant():
    assert c.analyser(entreprise(dette=None))[0] == c.INSUFFISANT


def test_jamais_positif_sans_fonds_islamique():
    assert c.niveau_final(c.MAJORITAIRE, [], "gardee") == c.MAJORITAIRE
    assert c.niveau_final(c.MAJORITAIRE, [], "ecartee") == c.ECARTEE
    assert c.niveau_final(c.MAJORITAIRE, [], "non_couverte") == c.NON_CONFIRMEE
    assert c.niveau_final(c.UNANIMITE, ["filiale de crédit"], "gardee") == c.A_VERIFIER
    assert c.niveau_final(c.NON_CONFORME, [], "gardee") == c.NON_CONFORME


def test_detecteur_activites_cachees():
    from agentbourse.alertes import detecter
    assert detecter("Discount Stores", "")
    assert detecter("Farm & Heavy Construction Machinery", "Its Financial Products segment offers loans")
    assert detecter("Beverages - Non-Alcoholic", "Sells beer and wine")
    assert not detecter("Beverages - Non-Alcoholic", "Sells non-alcoholic beverages")
    assert not detecter("Software - Infrastructure", "Develops software and cloud services")


def test_purification():
    assert c.purification(entreprise(revenus_interets=20)) == 0.02


def test_faute_de_frappe_corrigee():
    assert depuis_liste_connue("aple")[0].symbole == "AAPL"
    assert depuis_liste_connue("Total Energie")[0].symbole == "TTE.PA"
