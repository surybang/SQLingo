Vous êtes chargé d'analyser les revenus générés par les commandes en tenant compte des remises appliquées via des codes de réduction. Les remises sont appliquées comme suit :

- Si le code de réduction est DISCOUNT10, une réduction de 10% est appliquée sur le montant total de la commande.
- Si le code de réduction est DISCOUNT20, une réduction de 20% est appliquée sur le montant total de la commande.
- Si aucun code de réduction ou un code inconnu est utilisé, aucune remise n'est appliquée.

Écrivez une requête SQL qui calcule le revenu total pour chaque code de réduction, en tenant compte des remises appliquées.


Que remarquez-vous concernant les cas où discount_code est vide ou unknown ? 

Regardez la fonction COALESCE() pour obtenir un meilleur résultat. 