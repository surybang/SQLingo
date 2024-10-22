
WITH total_revenue AS(
SELECT discount_code, CASE
            WHEN discount_code = 'DISCOUNT10' THEN quantity * price_per_unit * 0.9
            WHEN discount_code = 'DISCOUNT20' THEN quantity * price_per_unit * 0.8
            ELSE quantity * price_per_unit
        END as total_revenue
FROM discount)

SELECT SUM(total_revenue) 
FROM
    total_revenue
GROUP BY 
    discount_code



-- CTE AVEC COALESCE
-- WITH total_revenue AS (
--     SELECT 
--         COALESCE(discount_code, 'UNKNOWN') AS discount_code, 
--         CASE
--             WHEN discount_code = 'DISCOUNT10' THEN quantity * price_per_unit * 0.9
--             WHEN discount_code = 'DISCOUNT20' THEN quantity * price_per_unit * 0.8
--             ELSE quantity * price_per_unit
--         END AS total_revenue
--     FROM discount
-- )

-- SELECT 
--     discount_code,
--     SUM(total_revenue) AS total_revenue
-- FROM
--     total_revenue
-- GROUP BY 
--     discount_code;


-- SANS CTE AVEC COALESCE 
-- SELECT COALESCE(discount_code, 'UNKNOWN') as discount_code, 
--        SUM(CASE
--             WHEN discount_code = 'DISCOUNT10' THEN quantity * price_per_unit * 0.9
--             WHEN discount_code = 'DISCOUNT20' THEN quantity * price_per_unit * 0.8
--             ELSE quantity * price_per_unit
--            END) as total_revenue
-- FROM discount
-- GROUP BY COALESCE(discount_code, 'UNKNOWN');
