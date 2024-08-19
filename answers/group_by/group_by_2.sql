SELECT 
    client,
    SUM(montant) AS total_amount
FROM ventes
GROUP BY client
HAVING SUM(montant) > 100
ORDER BY SUM(montant) DESC


-- P2 
-- SELECT 
--     client, 
--     SUM(montant) AS total_amount,
--     RANK() OVER (ORDER BY SUM(montant) DESC) AS rank
-- FROM 
--     ventes
-- GROUP BY 
--     client
-- HAVING SUM(montant) > 100


-- P3
-- SELECT 
--     client, 
--     SUM(montant) AS total_amount,
--     DENSE_RANK() OVER (ORDER BY SUM(montant) DESC) AS rank
-- FROM 
--     ventes
-- GROUP BY 
--     client
-- HAVING SUM(montant) > 100
