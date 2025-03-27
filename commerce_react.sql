/*
CREATE DATABASE commerce_react
*/

USE commerce_react;

/*
CREATE TABLE CustomerAccount (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(35),
    email VARCHAR(50),
    phone_number VARCHAR(15)
);

CREATE TABLE ProductCatalog (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(30),
    price DECIMAL(5, 2),
    stock_level INT,
    customer_id INT,
    FOREIGN KEY (customer_id) REFERENCES CustomerAccount(customer_id)
);
*/

/*
ALTER TABLE CustomerAccount
ADD COLUMN username VARCHAR(50) UNIQUE,
ADD COLUMN password VARCHAR(15);
*/

/*
ALTER TABLE ProductCatalog
DROP COLUMN order_date;
*/

/*
ALTER TABLE ProductCatalog
ADD COLUMN restock_items INT AFTER stock_level;
*/

/*
CREATE TABLE OrderManagement (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    place_order_date DATE,
    retrieve_order INT(8),
    track_order VARCHAR(50),
    manage_order_history VARCHAR(50),
    cancel_order BOOLEAN,
    cal_total_price DECIMAL(10, 2),
    customer_id INT,
    FOREIGN KEY (customer_id) REFERENCES CustomerAccount(customer_id)
);
*/

/*
INSERT INTO ProductCatalog (product_name, price, stock_level, customer_id) 
VALUES ('Sample Product', 99.99, 50, 1);
*/

SELECT * FROM ProductCatalog