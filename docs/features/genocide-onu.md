# Critère « liée à un génocide (selon l'ONU) »

## But
Ne jamais donner d'avis positif à une entreprise que l'ONU désigne comme impliquée dans la guerre à Gaza ou dans les colonies israéliennes.

## Sources (choisies par Salahdin le 20/11/2026)
1. **Rapport A/HRC/59/23** de Francesca Albanese, rapporteuse spéciale de l'ONU, « From economy of occupation to economy of genocide » (juillet 2025). Environ 48 à 60 entreprises citées (Microsoft, Alphabet, Amazon, IBM, Palantir, Caterpillar, Elbit…). C'est l'avis d'une experte indépendante de l'ONU, pas un jugement.
2. **Base de données du Haut-Commissariat de l'ONU aux droits de l'homme** sur les entreprises actives dans les colonies israéliennes (mise à jour du 26/09/2025 : 158 entreprises ; une mise à jour de 2026 serait à 214, à vérifier).

Contexte : le 16/09/2025, la commission d'enquête indépendante de l'ONU a conclu qu'Israël commet un génocide à Gaza. Israël rejette ces conclusions. La Cour internationale de justice n'a pas encore rendu son jugement final.

## Ce qu'on code
- `donnees_onu/entreprises.csv` (dans le dépôt, car ce sont des documents publics de l'ONU) : nom de l'entreprise, codes boursiers quand on les trouve, source, page ou paragraphe du rapport. Liste extraite à la main des annexes officielles, puis relue.
- `agentbourse/onu.py` : retrouve une action dans cette liste (par code, puis par nom, comme pour les ETF).
- Nouveau niveau **🟣 Liée à un génocide (selon l'ONU)**, avec la source affichée. Il passe avant les autres : jamais d'avis positif, même si les fonds islamiques gardent l'action.
- La légende explique d'où viennent les listes, et que c'est un critère éthique qu'on ajoute en plus des normes islamiques (les fonds MSCI et S&P ne l'appliquent pas : Microsoft et Google sont dans leurs ETF islamiques).
- Tests sans internet + rapport de comparaison mis à jour (combien des 150 grosses actions sont touchées).

## Ce qu'on ne fait pas
- Pas d'autres listes pour l'instant (Myanmar, etc.).
- Pas de jugement automatique à partir de l'actualité : seulement les listes officielles.
