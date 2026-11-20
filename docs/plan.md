# Plan — AgentBourse

## Où on en est
- 20/11/2026 : projet créé (règles, dépôt GitHub public). Le plan de la V1 vient du brainstorm (projet InvestHalal, qui fait doublon).
- 20/11/2026 : **analyseur halal, étape 1 codée** : recherche d'une action par son nom, tests selon 5 normes, échelle de conformité, légende, purification. Commande : `python analyser.py "nom de l'action"`.
- 20/11/2026 : chaque résultat porte la mention « selon les seules données publiques gratuites : à vérifier ».
- 20/11/2026 : **comparaison avec les ETF islamiques** (`comparer_etf.py`, rapport dans `docs/comparaison-etf.md`) : même avis que l'ETF MSCI World Islamic dans 86 % des cas, que l'ETF S&P 500 Sharia dans 81 %. Le cas grave (nous disons conforme, l'ETF écarte) touche surtout des activités interdites cachées : supermarchés (alcool, porc), divertissement et médias, filiales de crédit.

## Prochaine étape
- Faire relire l'échelle et la légende par Salahdin (et si possible par une personne de savoir).
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

### Partie 2 — Simulation en argent fictif (`agentbourse/simulation.py`, à faire)
- ETF iShares MSCI World Islamic (IE00B27YCN58), cours en euros, depuis 2015.
- Stratégie A : 70 €/mois chaque mois.
- Stratégie B : « bon moment » = on garde l'argent tant que le cours est au-dessus de sa moyenne sur 200 jours, on achète tout quand il passe dessous.
- Résultat après frais (réglables) et après flat tax 31,4 %, avec une courbe.

### Tableau de bord (Streamlit, à faire)
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
