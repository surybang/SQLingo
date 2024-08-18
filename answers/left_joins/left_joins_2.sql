SELECT c.customer_id, c.customer_name, p.product_id, p.product_name, od.quantity
FROM customers c 
LEFT JOIN orders o ON c.customer_id = o.customer_id
LEFT JOIN order_details od ON o.order_id = od.order_id
LEFT JOIN products p ON od.product_id = p.product_id