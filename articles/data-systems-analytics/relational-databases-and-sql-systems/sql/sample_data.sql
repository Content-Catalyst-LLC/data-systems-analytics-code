INSERT OR IGNORE INTO customers VALUES
    (1, 'ada@example.com', 'Ada Lovelace', '2025-01-03', 'active'),
    (2, 'grace@example.com', 'Grace Hopper', '2025-02-14', 'active'),
    (3, 'katherine@example.com', 'Katherine Johnson', '2025-03-22', 'inactive');

INSERT OR IGNORE INTO products VALUES
    (101, 'Sensor Kit', 'Instrumentation', 120.00),
    (102, 'Edge Board', 'Embedded Systems', 85.00),
    (103, 'Analytics License', 'Software', 300.00);

INSERT OR IGNORE INTO orders VALUES
    (1001, 1, '2026-05-01', 'paid'),
    (1002, 2, '2026-05-02', 'shipped'),
    (1003, 1, '2026-05-03', 'created');

INSERT OR IGNORE INTO order_lines VALUES
    (5001, 1001, 101, 2, 120.00),
    (5002, 1001, 102, 1, 85.00),
    (5003, 1002, 103, 1, 300.00),
    (5004, 1003, 102, 3, 85.00);

INSERT OR IGNORE INTO payments VALUES
    (7001, 1001, 'captured', 325.00, '2026-05-01T10:00:00Z'),
    (7002, 1002, 'captured', 300.00, '2026-05-02T11:00:00Z'),
    (7003, 1003, 'authorized', 255.00, '2026-05-03T12:00:00Z');

INSERT OR IGNORE INTO shipments VALUES
    (9001, 1002, 'shipped', '2026-05-04', '2026-05-03T15:00:00Z'),
    (9002, 1003, 'pending', '2026-05-06', NULL);

INSERT OR IGNORE INTO audit_log VALUES
    (1, 'orders', '1001', 'INSERT', 'etl_service', '2026-05-01T10:00:00Z'),
    (2, 'payments', '7001', 'INSERT', 'etl_service', '2026-05-01T10:00:01Z'),
    (3, 'shipments', '9001', 'INSERT', 'logistics_user', '2026-05-03T15:00:00Z');
