CREATE DATABASE IF NOT EXISTS lab_db;
USE lab_db;

-- 1. Roles Table
CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(100)
);

-- 2. Users Table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role_id INT NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(id)
);

-- 3. Products Table
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock INT DEFAULT 0
);

-- 4. System Config Table
CREATE TABLE system_config (
    id INT AUTO_INCREMENT PRIMARY KEY,
    config_key VARCHAR(100) NOT NULL UNIQUE,
    config_value TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ==========================================
-- DATA INSERTION
-- ==========================================

INSERT INTO roles (role_name, description) VALUES 
('admin', 'Administrator with full privileges'), 
('moderator', 'Content moderator'), 
('user', 'Standard registered user');

INSERT INTO users (role_id, username, email, password_hash) VALUES 
(1, 'admin', 'admin@company.local', '21232f297a57a5a743894a0e4a801fc3'),
(3, 'johndoe', 'john@company.local', '5f4dcc3b5aa765d61d8327deb882cf99'),
(3, 'alicesmith', 'alice@company.local', '7c6a180b36896a0a8c02787eeafb0e4c'),
(2, 'mod_pete', 'pete@company.local', '098f6bcd4621d373cade4e832627b4f6');

INSERT INTO products (name, price, stock) VALUES 
('Cybersecurity 101 Book', 29.99, 150),
('Mechanical Keyboard', 120.50, 45),
('Coffee Mug', 12.00, 300);


INSERT INTO system_config (config_key, config_value) VALUES 
('site_name', 'Vulnerable Dashboard v2.1'),
('maintenance_mode', 'false'),
('session_timeout', '3600'),
('api_master_secret', 'FLAG{4dv4nc3d_3num3r4t10n_m4st3r}');
