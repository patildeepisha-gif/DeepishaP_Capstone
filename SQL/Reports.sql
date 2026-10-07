Query 1
SELECT 
    COUNT(*) AS total_orders,
    
    SUM(quantity * price * (1 - COALESCE(discount_pct, 0) / 100.0)) AS total_revenue,
    
    AVG(quantity * price * (1 - COALESCE(discount_pct, 0) / 100.0)) AS average_order_value
FROM 
    orders o
JOIN 
    products p ON o.product_id = p.product_id;

Query 2
SELECT 
    COUNT(*) AS total_rows,
    COUNT(rating) AS non_null_ratings,
    (COUNT(*) - COUNT(rating)) AS missing_ratings_count
FROM 
    orders;

Query 3
SELECT 
    c.customer_id, 
    c.name, 
    COUNT(o.order_id) AS total_orders
FROM 
    customers c
LEFT JOIN 
    orders o ON c.customer_id = o.customer_id
GROUP BY 
    c.customer_id, 
    c.name
HAVING 
    COUNT(o.order_id) = 0;

SELECT 
    customer_id, 
    name
FROM 
    customers
WHERE 
    customer_id NOT IN (
        SELECT DISTINCT customer_id 
        FROM orders 
        WHERE customer_id IS NOT NULL
    );



