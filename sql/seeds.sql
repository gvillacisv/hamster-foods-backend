INSERT INTO customers (id, name) VALUES ('customer-001', 'Champion');

INSERT INTO orders (id, customer_id, amount_value, amount_currency, amount_base, exchange_rate, created_at) VALUES 
('order-c-hist1', 'customer-001', 8.50, 'EUR', 8.50, 1.0, datetime('now', '-120 days')),
('order-c-hist2', 'customer-001', 8.50, 'EUR', 8.50, 1.0, datetime('now', '-60 days')),
('order-c-hist3', 'customer-001', 7.00, 'EUR', 7.00, 1.0, datetime('now', '-30 days'));

INSERT INTO orders (id, customer_id, amount_value, amount_currency, amount_base, exchange_rate, created_at) VALUES 
('order-c-01', 'customer-001', 15.00, 'EUR', 15.00, 1.0, datetime('now', '-2 days', 'start of day', '+10 hours', '+31 minutes')),
('order-c-02', 'customer-001', 10.00, 'EUR', 10.00, 1.0, datetime('now', '-5 days', 'start of day', '+18 hours', '+05 minutes')),
('order-c-03', 'customer-001', 8.50, 'EUR', 8.50, 1.0, datetime('now', '-8 days', 'start of day', '+12 hours', '+15 minutes'));

INSERT INTO tier_history (id, customer_id, order_id, tier, date, total_base_at_change, change_reason) VALUES
('th-c1', 'customer-001', NULL, 'No Tier', datetime('now', '-180 days'), 0.00, 'TRANSACTION'),
('th-c2', 'customer-001', 'order-c-hist1', 'Rookie', datetime('now', '-120 days'), 8.50, 'TRANSACTION'),
('th-c3', 'customer-001', 'order-c-hist2', 'Loyal', datetime('now', '-60 days'), 17.00, 'TRANSACTION'),
('th-c4', 'customer-001', 'order-c-hist3', 'Champion', datetime('now', '-30 days'), 24.00, 'TRANSACTION');

INSERT INTO customers (id, name) VALUES ('customer-002', 'Loyal');

INSERT INTO orders (id, customer_id, amount_value, amount_currency, amount_base, exchange_rate, created_at) VALUES 
('order-l-hist1', 'customer-002', 10.00, 'EUR', 10.00, 1.0, datetime('now', '-45 days')),
('order-l-hist2', 'customer-002', 6.50, 'EUR', 6.50, 1.0, datetime('now', '-20 days'));

INSERT INTO orders (id, customer_id, amount_value, amount_currency, amount_base, exchange_rate, created_at) VALUES 
('order-l-01', 'customer-002', 10.00, 'EUR', 10.00, 1.0, datetime('now', '-1 days', 'start of day', '+11 hours', '+45 minutes')),
('order-l-02', 'customer-002', 8.00, 'EUR', 8.00, 1.0, datetime('now', '-8 days', 'start of day', '+16 hours', '+30 minutes'));

INSERT INTO tier_history (id, customer_id, order_id, tier, date, total_base_at_change, change_reason) VALUES
('th-l1', 'customer-002', NULL, 'No Tier', datetime('now', '-90 days'), 0.00, 'TRANSACTION'),
('th-l2', 'customer-002', 'order-l-hist1', 'Rookie', datetime('now', '-45 days'), 10.00, 'TRANSACTION'),
('th-l3', 'customer-002', 'order-l-hist2', 'Loyal', datetime('now', '-20 days'), 16.50, 'TRANSACTION');

INSERT INTO customers (id, name) VALUES ('customer-003', 'Rookie');

INSERT INTO orders (id, customer_id, amount_value, amount_currency, amount_base, exchange_rate, created_at) VALUES 
('order-r-hist1', 'customer-003', 7.50, 'EUR', 7.50, 1.0, datetime('now', '-15 days', 'start of day', '+15 hours', '+00 minutes'));

INSERT INTO orders (id, customer_id, amount_value, amount_currency, amount_base, exchange_rate, created_at) VALUES 
('order-r-01', 'customer-003', 10.00, 'EUR', 10.00, 1.0, datetime('now', '-3 days', 'start of day', '+13 hours', '+00 minutes'));

INSERT INTO tier_history (id, customer_id, order_id, tier, date, total_base_at_change, change_reason) VALUES
('th-r1', 'customer-003', NULL, 'No Tier', datetime('now', '-30 days'), 0.00, 'TRANSACTION'),
('th-r2', 'customer-003', 'order-r-hist1', 'Rookie', datetime('now', '-15 days', 'start of day', '+15 hours', '+01 minutes'), 7.50, 'TRANSACTION');

INSERT INTO customers (id, name) VALUES ('customer-004', 'Newbie');

INSERT INTO orders (id, customer_id, amount_value, amount_currency, amount_base, exchange_rate, created_at) VALUES 
('order-n-01', 'customer-004', 5.00, 'EUR', 5.00, 1.0, datetime('now', '-4 days', 'start of day', '+17 hours', '+50 minutes'));

INSERT INTO tier_history (id, customer_id, order_id, tier, date, total_base_at_change, change_reason) VALUES
('th-n1', 'customer-004', 'order-n-01', 'No Tier', datetime('now', '-4 days', 'start of day', '+17 hours', '+51 minutes'), 5.00, 'TRANSACTION');

INSERT INTO customers (id, name) VALUES ('customer-005', 'Demoted');

INSERT INTO orders (id, customer_id, amount_value, amount_currency, amount_base, exchange_rate, created_at) VALUES 
('order-d-hist1', 'customer-005', 9.00, 'EUR', 9.00, 1.0, datetime('now', '-15 days', 'start of day', '+08 hours', '+12 minutes'));

INSERT INTO tier_history (id, customer_id, order_id, tier, date, total_base_at_change, change_reason) VALUES
('th-d1', 'customer-005', NULL, 'No Tier', datetime('now', '-60 days'), 0.00, 'TRANSACTION'),
('th-d2', 'customer-005', 'order-d-hist1', 'Rookie', datetime('now', '-15 days', 'start of day', '+08 hours', '+13 minutes'), 9.00, 'TRANSACTION'),
('th-d3', 'customer-005', NULL, 'No Tier', datetime('now', '-1 days'), 0.00, 'EXPIRATION');