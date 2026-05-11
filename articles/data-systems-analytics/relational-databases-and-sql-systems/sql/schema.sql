PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    customer_name TEXT NOT NULL,
    created_at TEXT NOT NULL,
    customer_status TEXT NOT NULL CHECK (customer_status IN ('active', 'inactive', 'suspended'))
);

CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    product_category TEXT NOT NULL,
    price REAL NOT NULL CHECK (price >= 0)
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('created', 'paid', 'shipped', 'cancelled')),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS order_lines (
    order_line_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price REAL NOT NULL CHECK (unit_price >= 0),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE IF NOT EXISTS payments (
    payment_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    payment_status TEXT NOT NULL CHECK (payment_status IN ('authorized', 'captured', 'failed', 'refunded')),
    amount REAL NOT NULL CHECK (amount >= 0),
    payment_time TEXT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

CREATE TABLE IF NOT EXISTS shipments (
    shipment_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    shipment_status TEXT NOT NULL CHECK (shipment_status IN ('pending', 'shipped', 'delayed', 'delivered')),
    promised_date TEXT NOT NULL,
    shipped_at TEXT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

CREATE TABLE IF NOT EXISTS audit_log (
    audit_id INTEGER PRIMARY KEY,
    table_name TEXT NOT NULL,
    record_id TEXT NOT NULL,
    action_type TEXT NOT NULL CHECK (action_type IN ('INSERT', 'UPDATE', 'DELETE', 'GRANT', 'REVOKE')),
    actor_role TEXT NOT NULL,
    action_time TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_orders_customer_date ON orders(customer_id, order_date);
CREATE INDEX IF NOT EXISTS idx_orders_date_status ON orders(order_date, status);
CREATE INDEX IF NOT EXISTS idx_order_lines_order_product ON order_lines(order_id, product_id);
CREATE INDEX IF NOT EXISTS idx_payments_order_status ON payments(order_id, payment_status);
CREATE INDEX IF NOT EXISTS idx_shipments_status_promised ON shipments(shipment_status, promised_date);
CREATE INDEX IF NOT EXISTS idx_audit_action_actor ON audit_log(action_type, actor_role);
