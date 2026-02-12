-- Using MySQL-compatible syntax for SQLite

DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS tier_history;

CREATE TABLE customers (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE orders (
    id VARCHAR(255) PRIMARY KEY,
    customer_id VARCHAR(255) NOT NULL,
    amount_value DECIMAL(10, 2) NOT NULL,
    amount_currency VARCHAR(3) NOT NULL,
    amount_base DECIMAL(10, 2) NOT NULL,
    exchange_rate DECIMAL(10, 6) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE tier_history (
    id VARCHAR(255) PRIMARY KEY,
    customer_id VARCHAR(255) NOT NULL,
    order_id VARCHAR(255) NULL,
    tier VARCHAR(50) NOT NULL,
    date TIMESTAMP NOT NULL,
    total_base_at_change DECIMAL(10, 2) NOT NULL,
    change_reason VARCHAR(20) NOT NULL CHECK(change_reason IN ('TRANSACTION', 'EXPIRATION')),
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (order_id) REFERENCES orders(id)
);
