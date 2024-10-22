SELECT 
    c.customer_name,
    s.store_id,
    sp.product_id,
    p.product_name,
    p.product_price
FROM 
    df_customers c
FULL OUTER JOIN df_stores s ON c.customer_id = s.customer_id
FULL OUTER JOIN df_store_products sp ON s.store_id = sp.store_id
FULL OUTER JOIN df_products p ON sp.product_id = p.product_id
ORDER BY c.customer_name, s.store_id, sp.product_id
