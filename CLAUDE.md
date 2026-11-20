# AgentBourse — règles du projet

## Le projet

Un agent (programme) qui investit en bourse : il récupère les cours, applique une stratégie, et décide d'acheter ou de vendre.
**Il commence en argent fictif (« paper trading »)** : aucun euro réel n'est engagé tant que Salahdin n'a pas décidé, lui-même, de passer au réel.

## Qui te parle

Salahdin, qui **débute en développement**.
- Parle simplement, en français, sans jargon non expliqué. Une phrase sur le *pourquoi* quand c'est utile.
- Il dicte souvent à la voix : les messages peuvent contenir des mots mal transcrits. Interprète, et demande en cas de vrai doute.
- Avance par petits pas testables. Pour une grosse étape, propose un plan court et attends son accord.

## Règles

**Au début de chaque session, lis `docs/plan.md`.** Mets-le à jour à la fin de chaque étape.
**Chaque fois que tu codes, charge d'abord le skill `coder-comme-un-senior`.**

- **Dépôt GitHub public** : aucune clé d'API, aucun mot de passe dans le code. Les secrets vont dans un fichier `.env` (ignoré par git) ; un `.env.example` montre les noms sans les valeurs.
- **Les nombres réglables** (montant par ordre, seuils, période des moyennes…) vont dans un fichier de configuration, pas en dur dans le code.
- **Sécurité de l'argent** : le mode fictif est le mode par défaut. Passer au réel demande un réglage explicite de Salahdin, jamais un changement fait par Claude de lui-même.
- Ce projet n'est pas un conseil en investissement : les stratégies sont des expériences.
