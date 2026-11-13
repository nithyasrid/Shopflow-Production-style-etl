-- Revenue by snapshot date (the source API does not expose purchase timestamps)
SELECT d.full_date AS snapshot_date, COUNT(DISTINCT f.order_id) AS orders,
       SUM(f.line_total) AS gross_merchandise_value
FROM fact_order_items f JOIN dim_date d USING (date_key)
GROUP BY d.full_date ORDER BY d.full_date DESC;

-- Top products by sales value
SELECT p.product_id, p.title, SUM(f.quantity) AS units,
       SUM(f.line_total) AS sales_value
FROM fact_order_items f JOIN dim_product p USING (product_key)
GROUP BY p.product_id, p.title ORDER BY sales_value DESC LIMIT 10;

-- Top customers by order value
SELECT c.customer_id, COUNT(DISTINCT f.order_id) AS orders,
       SUM(f.line_total) AS sales_value
FROM fact_order_items f JOIN dim_customer c USING (customer_key)
GROUP BY c.customer_id ORDER BY sales_value DESC LIMIT 10;
