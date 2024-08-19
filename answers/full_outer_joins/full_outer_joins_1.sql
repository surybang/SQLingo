SELECT * 
FROM df_store_products
FULL OUTER JOIN df_products
USING (product_id)