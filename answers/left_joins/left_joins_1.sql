SELECT 
    p.product_id, 
    p.product_name, 
    p.product_price, 
    od.quantity, 
    od.order_id
FROM products p
LEFT JOIN order_details od
on p.product_id = od.product_id