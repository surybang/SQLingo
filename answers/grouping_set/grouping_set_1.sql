WITH sales_totals AS (
    SELECT store_id, 
    COALESCE(product_name, 'tout_le_magasin') AS product_name,
    SUM(amount) as sum_amount 
    FROM redbull
    GROUP BY 
    GROUPING SETS ((store_id, product_name), store_id)
    ORDER BY store_id
)

SELECT 
    ls.store_id,
    ls.product_name AS l_product_name, 
    rs.product_name AS r_product_name, 
    ls.sum_amount as product_sum_amount,
    rs.sum_amount as store_sum_amount, 
    product_sum_amount / store_sum_amount as product_pct
FROM sales_totals ls 
INNER JOIN sales_totals rs
USING (store_id)
WHERE ls.product_name = 'redbull' AND rs.product_name = 'tout_le_magasin'
ORDER BY store_id, l_product_name



-- SANS GROUPING SETS
-- WITH total_sales AS (
-- SELECT store_id, SUM(amount) as total_sales
-- FROM redbull
-- GROUP BY
-- store_id
-- ),

-- pct_sales AS (
-- SELECT *, amount/total_sales AS pct_sales 
-- FROM redbull
-- LEFT JOIN total_sales
-- USING (store_id)
-- )

-- SELECT store_id, sum(amount), total_sales, SUM(pct_sales) AS product_pct_of_sales
-- FROM pct_sales
-- WHERE product_name = 'redbull'
-- GROUP BY store_id, total_sales