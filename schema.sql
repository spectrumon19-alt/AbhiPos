-- PostgreSQL Database Schema for POS System

-- Users table
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR UNIQUE NOT NULL,
    password_hash VARCHAR NOT NULL,
    role VARCHAR NOT NULL CHECK (role IN ('Admin', 'Cashier')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products table
CREATE TABLE IF NOT EXISTS products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    pack_size VARCHAR,
    sku VARCHAR UNIQUE,
    gst_rate DECIMAL(5, 2) NOT NULL,
    purchase_rate DECIMAL(10, 2),
    selling_rate DECIMAL(10, 2) NOT NULL
);

-- Inventory table
CREATE TABLE IF NOT EXISTS inventory (
    product_id INTEGER PRIMARY KEY REFERENCES products(product_id),
    stock_quantity INTEGER NOT NULL DEFAULT 0
);

-- Sales invoices table
CREATE TABLE IF NOT EXISTS sales_invoices (
    invoice_id SERIAL PRIMARY KEY,
    invoice_number VARCHAR UNIQUE NOT NULL,
    invoice_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    customer_name VARCHAR,
    customer_contact VARCHAR,
    user_id INTEGER REFERENCES users(user_id),
    mode_of_payment VARCHAR,
    total_amount DECIMAL(10, 2) NOT NULL,
    total_gst DECIMAL(10, 2) NOT NULL,
    status VARCHAR DEFAULT 'Completed' CHECK (status IN ('Completed', 'Cancelled'))
);

-- Sales invoice items table
CREATE TABLE IF NOT EXISTS sales_invoice_items (
    item_id SERIAL PRIMARY KEY,
    invoice_id INTEGER REFERENCES sales_invoices(invoice_id),
    product_id INTEGER REFERENCES products(product_id),
    quantity INTEGER NOT NULL,
    rate_at_sale DECIMAL(10, 2) NOT NULL,
    gst_rate_at_sale DECIMAL(5, 2) NOT NULL,
    exclusive_gst_amount DECIMAL(10, 2) NOT NULL,
    sgst DECIMAL(10, 2) NOT NULL,
    cgst DECIMAL(10, 2) NOT NULL,
    total_line_amount DECIMAL(10, 2) NOT NULL
);

-- Sample data for testing (only insert if tables are empty)
INSERT INTO users (username, password_hash, role) 
SELECT 'admin', '$pbkdf2-sha256$29000$xLj3fs9Zi7E2ZgxhrBUixA$xufNJFzqPmmSAS2pnMraPuQUbE1yWEld2UAYJBmP0aj8', 'Admin'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = 'admin');

INSERT INTO users (username, password_hash, role) 
SELECT 'cashier', '$pbkdf2-sha256$29000$rJUyZqyVkpLyHoMwZsy51w$M7F9vPmL0AsyWFgHhXgLWU4P9r6IjHQ1BjoBz6Naz.0', 'Cashier'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = 'cashier');

INSERT INTO products (name, pack_size, sku, gst_rate, purchase_rate, selling_rate) 
SELECT 'Product A', '1 kg', 'PROD-A-001', 18.00, 80.00, 100.00
WHERE NOT EXISTS (SELECT 1 FROM products WHERE sku = 'PROD-A-001');

INSERT INTO products (name, pack_size, sku, gst_rate, purchase_rate, selling_rate) 
SELECT 'Product B', '500 g', 'PROD-B-002', 12.00, 45.00, 60.00
WHERE NOT EXISTS (SELECT 1 FROM products WHERE sku = 'PROD-B-002');

INSERT INTO products (name, pack_size, sku, gst_rate, purchase_rate, selling_rate) 
SELECT 'Product C', '1 piece', 'PROD-C-003', 5.00, 25.00, 30.00
WHERE NOT EXISTS (SELECT 1 FROM products WHERE sku = 'PROD-C-003');

INSERT INTO inventory (product_id, stock_quantity) 
SELECT 1, 100
WHERE NOT EXISTS (SELECT 1 FROM inventory WHERE product_id = 1);

INSERT INTO inventory (product_id, stock_quantity) 
SELECT 2, 200
WHERE NOT EXISTS (SELECT 1 FROM inventory WHERE product_id = 2);

INSERT INTO inventory (product_id, stock_quantity) 
SELECT 3, 150
WHERE NOT EXISTS (SELECT 1 FROM inventory WHERE product_id = 3);