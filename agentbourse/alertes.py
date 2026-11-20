"""Détecter les activités interdites « cachées » : celles que les chiffres ne montrent pas.

Deux sources gratuites :
  1. l'activité donnée par Yahoo (ex. « Discount Stores » = supermarché, qui vend souvent alcool et porc) ;
  2. la description de l'entreprise (ex. « Financial Products segment » = filiale de crédit).
Une alerte ne dit pas « interdit » : elle dit « à vérifier ».
"""
import re

from agentbourse import config


def detecter(activite: str, description: str) -> list[str]:
    """Liste des raisons de se méfier (vide si rien trouvé)."""
    alertes = []
    raison = config.ACTIVITES_A_RISQUE.get(activite)
    if raison:
        alertes.append(f"{raison} (activité : {activite})")
    for motif, raison in config.PHRASES_A_RISQUE.items():
        trouve = re.search(motif, description, re.IGNORECASE)
        if trouve:
            alertes.append(f"{raison} (« {trouve.group(0)} »)")
    return alertes
