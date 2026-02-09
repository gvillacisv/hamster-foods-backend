INSERT INTO customers (id, name) VALUES ('customer-001', 'Champion');

-- Orders in the last 10 days
INSERT INTO orders (id, customer_id, amount_value, amount_currency, amount_base, exchange_rate, created_at) VALUES 
('order-001', 'customer-001', 15.00, 'EUR', 15.00, 1.0, datetime('now', '-2 days')),
('order-002', 'customer-001', 10.00, 'EUR', 10.00, 1.0, datetime('now', '-5 days'));

-- Order outside the 10 day window (should not be counted)
INSERT INTO orders (id, customer_id, amount_value, amount_currency, amount_base, exchange_rate, created_at) VALUES 
('order-003', 'customer-001', 50.00, 'EUR', 50.00, 1.0, datetime('now', '-20 days'));

-- Tier History
INSERT INTO tier_history (id, customer_id, tier, date, total_base_at_change, change_reason) VALUES
('th-c1', 'customer-001', 'No Tier', '2024-01-10 09:15:00', 0.00, 'TRANSACTION'),
('th-c2', 'customer-001', 'Rookie', '2024-02-15 14:00:00', 8.50, 'TRANSACTION'),
('th-c3', 'customer-001', 'Loyal', '2024-04-20 11:30:00', 17.00, 'TRANSACTION'),
('th-c4', 'customer-001', 'Champion', '2024-06-01 18:45:00', 24.00, 'TRANSACTION');

-- ------------------------------------------------
-- User 2: "Loyal Lucy" - Should be Loyal Tier (Total: 18.00 EUR)
-- ------------------------------------------------
INSERT INTO customers (id, name) VALUES ('customer-002', 'Loyal Lucy');

-- Orders in the last 10 days
INSERT INTO orders (id, customer_id, amount_value, amount_currency, amount_base, exchange_rate, created_at) VALUES 
('order-004', 'customer-002', 10.00, 'EUR', 10.00, 1.0, datetime('now', '-1 days')),
('order-005', 'customer-002', 8.00, 'EUR', 8.00, 1.0, datetime('now', '-8 days'));

-- Tier History
INSERT INTO tier_history (id, customer_id, tier, date, total_base_at_change, change_reason) VALUES
('th-l1', 'customer-002', 'No Tier', '2024-03-05 10:00:00', 0.00, 'TRANSACTION'),
('th-l2', 'customer-002', 'Rookie', '2024-05-11 12:20:00', 10.00, 'TRANSACTION'),
('th-l3', 'customer-002', 'Loyal', '2024-07-01 20:00:00', 16.50, 'TRANSACTION');

-- ------------------------------------------------
-- User 3: "Rookie Rick" - Should be Rookie Tier (Total: 10.00 EUR)
-- ------------------------------------------------
INSERT INTO customers (id, name) VALUES ('customer-003', 'Rookie Rick');

-- Orders in the last 10 days
INSERT INTO orders (id, customer_id, amount_value, amount_currency, amount_base, exchange_rate, created_at) VALUES 
('order-006', 'customer-003', 10.00, 'EUR', 10.00, 1.0, datetime('now', '-3 days'));

-- Tier History
INSERT INTO tier_history (id, customer_id, tier, date, total_base_at_change, change_reason) VALUES
('th-r1', 'customer-003', 'No Tier', '2024-06-10 08:00:00', 0.00, 'TRANSACTION'),
('th-r2', 'customer-003', 'Rookie', '2024-07-15 13:05:00', 7.50, 'TRANSACTION');

-- ------------------------------------------------
-- User 4: "Newbie Nate" - Should be No Tier (Total: 5.00 EUR)
-- ------------------------------------------------
INSERT INTO customers (id, name) VALUES ('customer-004', 'Newbie Nate');

-- Orders in the last 10 days
INSERT INTO orders (id, customer_id, amount_value, amount_currency, amount_base, exchange_rate, created_at) VALUES 
('order-007', 'customer-004', 5.00, 'EUR', 5.00, 1.0, datetime('now', '-4 days'));

-- Tier History
INSERT INTO tier_history (id, customer_id, tier, date, total_base_at_change, change_reason) VALUES
('th-n1', 'customer-004', 'No Tier', '2024-07-20 16:00:00', 0.00, 'TRANSACTION');

-- ------------------------------------------------
-- Original Test User: "Fuzzy Hamster" - Should be Loyal Tier (Total: 21.44 EUR)
-- ------------------------------------------------
INSERT INTO customers (id, name) VALUES ('c123-e456-i789', 'Fuzzy Hamster');

-- Orders in the last 10 days
INSERT INTO orders (id, customer_id, amount_value, amount_currency, amount_base, exchange_rate, created_at) VALUES 
('order-008', 'c123-e456-i789', 12.00, 'EUR', 12.00, 1.0, datetime('now', '-2 days')),
('order-009', 'c123-e456-i789', 8.00, 'GBP', 9.44, 1.18, datetime('now', '-5 days')); -- 8 GBP * 1.18 = 9.44 EUR

-- Tier History
INSERT INTO tier_history (id, customer_id, tier, date, total_base_at_change, change_reason) VALUES
('th-f1', 'c123-e456-i789', 'No Tier', '2024-07-15 10:00:00', 0.00, 'TRANSACTION'),
('th-f2', 'c123-e456-i789', 'Rookie', '2024-07-20 11:30:00', 8.50, 'TRANSACTION'),
('th-f3', 'c123-e456-i789', 'Loyal', '2024-07-20 18:00:00', 16.00, 'TRANSACTION');