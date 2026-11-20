# Indice AgentBourse + agent de suivi en argent fictif

## But
Transformer nos règles en un **indice** (une liste d'actions et leurs poids, fixée par des règles écrites), puis le suivre chaque jour **en argent fictif**, automatiquement, pour construire un historique réel et public (CV, puis base d'un futur club ou ETF).

## Règles de l'indice (choisies par Salahdin le 20/11/2026)
- **Univers de départ** : les actions des fonds iShares MSCI World Islamic et MSCI EM Islamic (environ 800 actions, monde entier et pays émergents).
- **Entrée dans l'indice** : résultat final « 🟢 Conforme (avis majoritaire) » ou « ✅ unanimité ». Donc :
  passe la norme AAOIFI, gardée par au moins un fonds islamique, pas citée par l'ONU, aucune alerte d'activité cachée.
- **Répartition** : selon la valeur en bourse, **aucune action au-dessus de 5 %** (le surplus est redistribué aux autres).
- **Pas d'or** pour l'instant : actions seulement.
- **Réajustement** : complet 4 fois par an (après chaque saison de résultats). Pas de vente parce qu'un cours baisse.

## Ce que fait l'agent (chaque jour de bourse, automatiquement)
1. Calcule la valeur de l'indice et du portefeuille fictif (départ : 10 000 € fictifs le jour du lancement).
2. **Surveille la conformité** de chaque action de l'indice :
   - nouvelle citation par l'ONU, ou action sortie de tous les fonds islamiques → **sortie immédiate** ;
   - le reste (dette, intérêts) est revérifié au réajustement trimestriel.
3. Écrit un **journal** lisible : ce qui a été acheté, vendu, et pourquoi.

## Où ça tourne
**GitHub Actions** (gratuit pour un dépôt public) : l'agent tourne sur les serveurs de GitHub chaque soir après la fermeture de Wall Street, même si ton ordinateur est éteint, et enregistre ses résultats dans le dépôt. L'historique est donc public et daté : personne ne peut dire qu'il a été trafiqué après coup.

## Fichiers
- `agentbourse/indice.py` : sélection, poids plafonnés, valeur du jour.
- `agent_quotidien.py` : le travail de chaque soir.
- `indice/composition.csv`, `indice/historique.csv`, `indice/journal.md` : résultats publics.
- `.github/workflows/agent.yml` : le réveil automatique.
- Nouvel onglet du tableau de bord : composition, courbe depuis le lancement, journal.
- Tests sans internet (plafond de 5 %, sortie d'une action citée, calcul de la valeur).

## Limites assumées
- Données gratuites (Yahoo) : à vérifier, comme partout dans le projet.
- Pas de frais ni d'impôts dans l'indice lui-même (comme un indice officiel) ; le portefeuille fictif, lui, compte 0,1 % de frais par achat ou vente.
- Analyser ~800 actions prend environ 30 minutes : fait seulement au réajustement, pas chaque jour.
