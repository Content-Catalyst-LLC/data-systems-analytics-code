-- 1. Customer order history.
SELECT c.customer_id, c.customer_name, o.order_id, o.order_date, o.status,
       SUM(ol.quantity * ol.unit_price) AS order_value
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
JOIN order_lines ol ON ol.order_id = o.order_id
GROUP BY c.customer_id, c.customer_name, o.order_id, o.order_date, o.status
ORDER BY o.order_date DESC;

-- 2. Daily revenue report.
SELECT o.order_date,
       p.payment_status,
       SUM(p.amount) AS total_payment_amount,
       COUNT(DISTINCT o.order_id) AS order_count
FROM orders o
JOIN payments p ON p.order_id = o.order_id
GROUP BY o.order_date, p.payment_status
ORDER BY o.order_date;

-- 3. Product sales rank.
SELECT pr.product_id, pr.product_name,
       SUM(ol.quantity) AS units_sold,
       SUM(ol.quantity * ol.unit_price) AS gross_sales
FROM products pr
JOIN order_lines ol ON ol.product_id = pr.product_id
GROUP BY pr.product_id, pr.product_name
ORDER BY gross_sales DESC;

-- 4. Payment exception review.
SELECT p.payment_id, p.order_id, p.payment_status, p.amount, o.status AS order_status
FROM payments p
JOIN orders o ON o.order_id = p.order_id
WHERE p.payment_status IN ('failed', 'refunded', 'authorized')
ORDER BY p.payment_time DESC;

-- 5. Shipment delay monitor.
SELECT s.shipment_id, s.order_id, s.shipment_status, s.promised_date, o.order_date
FROM shipments s
JOIN orders o ON o.order_id = s.order_id
WHERE s.shipment_status IN ('pending', 'delayed')
ORDER BY s.promised_date;

-- 6. Audit access review.
SELECT action_type, actor_role, COUNT(*) AS event_count
FROM audit_log
GROUP BY action_type, actor_role
ORDER BY event_count DESC;
