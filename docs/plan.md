# Plan — AgentBourse

## Où on en est
- 20/11/2026 : projet créé (règles, dépôt GitHub public). Le plan de la V1 vient du brainstorm (projet InvestHalal, qui fait doublon).
- 20/11/2026 : **analyseur halal, étape 1 codée** : recherche d'une action par son nom, tests selon 5 normes, échelle de conformité, légende, purification. Commande : `python analyser.py "nom de l'action"`.
- 20/11/2026 : chaque résultat porte la mention « selon les seules données publiques gratuites : à vérifier ».
- 20/11/2026 : **comparaison avec les ETF islamiques** (`comparer_etf.py`, rapport dans `docs/comparaison-etf.md`) : même avis que l'ETF MSCI World Islamic dans 86 % des cas, que l'ETF S&P 500 Sharia dans 81 %. Le cas grave (nous disons conforme, l'ETF écarte) touche surtout des activités interdites cachées : supermarchés (alcool, porc), divertissement et médias, filiales de crédit.
- 20/11/2026 : **deux vérifications** dans l'analyseur : (1) notre calcul + un détecteur d'activités cachées (supermarché, filiale de crédit, divertissement…, réglages dans `config.py`) ; (2) l'avis de 4 fonds islamiques (iShares MSCI World / USA / EM Islamic, SP Funds S&P 500 Sharia), téléchargés automatiquement chaque semaine. **Règle : jamais d'avis positif sans un fonds islamique qui garde l'action.** Sur les 150 plus grosses actions, 28 cas graves sans cette règle ; le détecteur seul en attrape 12, la règle bloque les 28.
- 20/11/2026 : **troisième vérification, critère éthique ONU** (`agentbourse/onu.py`, liste dans `donnees_onu/entreprises.csv`, 188 entreprises avec leur source) : rapport Albanese A/HRC/59/23 + base ONU des colonies A/HRC/60/19. Niveau 🟣 « Citée par l'ONU », jamais d'avis positif. Sur les 150 plus grosses actions : 13 citées, dont 7 gardées par un fonds islamique (Microsoft, Alphabet, Chevron, IBM, Booking, BP). Plan : `docs/features/genocide-onu.md`.
- 20/11/2026 : **partie 2, simulation en argent fictif** (`python simuler.py`, réglages dans `config.py`, courbe dans `docs/simulation.png`) : ETF MSCI World Islamic en euros, 70 €/mois de janv. 2015 à nov. 2026, 10 010 € versés. A (chaque mois) : 16 147 € nets après frais et flat tax ; B (sous la moyenne 200 jours) : 16 352 €. L'écart (+205 €) vient surtout des frais (53 achats au lieu de 143) ; sans frais, B ne gagne que 91 €.

- 20/11/2026 : **tableau de bord** (`app.py`, Streamlit) : onglet analyseur (recherche, choix de l'action, 3 vérifications, légende) et onglet simulation (curseurs : versement, frais, moyenne, date de début ; tableau et courbe). Lancer : `.venv/Scripts/streamlit run app.py`.

## Prochaine étape
- Simulation avec un panier d'actions filtré par notre analyseur (l'ETF contient Microsoft et Google, cités par l'ONU).
- Mettre le tableau de bord en ligne (Streamlit Community Cloud, gratuit) pour le CV.
- Vérifier la mise à jour 2026 de la base ONU des colonies (214 entreprises annoncées) et compléter la liste.
- Faire relire l'échelle et la légende par Salahdin (et si possible par une personne de savoir).
- Améliorer le détecteur : 16 cas graves lui échappent encore (Coca-Cola, Nestlé, Pfizer, ADP…), voir `docs/comparaison-etf.md`.
- Comparer nos résultats à la liste officielle malaisienne (publiée deux fois par an) pour mesurer nos erreurs.
- Partie 2 : la simulation en argent fictif (voir plus bas).

## Version 1

### Partie 1 — Analyseur halal (`agentbourse/`)
- **Actions du monde entier** (Yahoo Finance), y compris les bourses des pays musulmans. Une action de pays musulman n'est pas halal d'office : elle passe le même test.
- **Recherche par nom** : la personne tape un nom, même mal écrit (« aple »). Le programme propose les actions qui ressemblent et demande « c'est bien celle-là ? ».
- **5 normes testées** (seuils dans `agentbourse/config.py`) :
  | Norme | Dette | Trésorerie et placements | Revenus d'intérêts | Comparé à |
  |---|---|---|---|---|
  | Stricte | 0 % | — | 0 % | — |
  | AAOIFI (norme 21) | < 30 % | < 30 % | < 5 % du CA | valeur en bourse |
  | S&P Shariah | < 33 % | < 33 % | < 5 % du CA | valeur en bourse moyenne sur 36 mois |
  | MSCI Islamic | < 33,33 % | < 33,33 % | < 5 % du CA | total du bilan |
  | Malaisie (SC) | < 33 % | < 33 % | < 5 % du CA | total du bilan |
  Plus, pour toutes : un secteur non interdit (banque, assurance, alcool, tabac, jeux, armement…).
- **Échelle** (expliquée dans la légende affichée en haut) :
  1. ✅ **Conforme à l'unanimité** : passe la norme stricte et les 4 autres.
  2. 🟢 **Conforme (avis majoritaire)** : passe la norme AAOIFI.
  3. 🟡 **(Conforme) avis minoritaire** : échoue à l'AAOIFI mais passe au moins une norme plus souple.
  4. 🔴 **Non conforme** : échoue partout, ou secteur interdit.
  5. ⚪ **Données insuffisantes** : on ne peut pas trancher.
- **Purification** : part du dividende à donner en aumône = revenus d'intérêts ÷ chiffre d'affaires.

### Partie 2 — Simulation en argent fictif (`agentbourse/simulation.py`, faite)
- ETF iShares MSCI World Islamic (IE00B27YCN58), cours en euros, depuis 2015.
- Stratégie A : 70 €/mois chaque mois.
- Stratégie B : « bon moment » = on garde l'argent tant que le cours est au-dessus de sa moyenne sur 200 jours, on achète tout quand il passe dessous.
- Résultat après frais (réglables) et après flat tax 31,4 %, avec une courbe.

### Tableau de bord (Streamlit, fait)
Un onglet par partie. L'analyseur y aura une barre de recherche.

## Plus tard (V2)
- Copier les dépôts 13F de grands investisseurs (filtrés halal).
- Résumé d'actualité optionnel avec Haiku 5.5.
- README pour recruteur : captures, résultats chiffrés, démo en ligne (Streamlit Community Cloud).

## Décisions prises
- Argent **fictif uniquement**, aucun ordre réel, aucun conseil personnalisé.
- Le programme ne dit jamais « halal » tout court : il dit **selon quelle norme**, avec une légende et un avertissement (outil de tri, ne remplace pas un savant).
- Le niveau le plus haut s'appelle « Conforme à l'unanimité » et pas « 100 % halal » : les chiffres viennent de Yahoo Finance et peuvent être faux ou incomplets.
- Données : Yahoo Finance (monde entier) plutôt que la SEC (États-Unis seulement).
- Pas d'appel IA dans le moteur de calcul. Nombres réglables dans `agentbourse/config.py`.
- Dépôt public : aucune clé ni donnée perso dans le code.
