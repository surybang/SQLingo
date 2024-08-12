SELECT client, MEAN(montant) as total_ventes
FROM ventes
GROUP BY client