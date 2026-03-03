CREATE DATABASE FoodDeliveryDB;
USE FoodDeliveryDB;

CREATE TABLE Customer (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    phone VARCHAR(20),
    date_created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO Customer (first_name, last_name, email, phone)
VALUES
('John', 'Doe', 'john@email.com', '555-1111'),
('Jane', 'Smith', 'jane@email.com', '555-2222');

CREATE TABLE Restaurant (
    restaurant_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(150) NOT NULL,
    address VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    cuisine_type VARCHAR(100),
    rating DECIMAL(3,2)
);

INSERT INTO Restaurant (name, address, phone, cuisine_type, rating)
VALUES
('Pizza Palace', '123 Main St', '555-3333', 'Italian', 4.5),
('Sushi House', '456 Elm St', '555-4444', 'Japanese', 4.8);

CREATE TABLE Driver (
    driver_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    license_number VARCHAR(50) NOT NULL UNIQUE,
    vehicle_type VARCHAR(50) NOT NULL,
    availability_status VARCHAR(50) NOT NULL
);

INSERT INTO Driver (first_name, last_name, license_number, vehicle_type, availability_status)
VALUES
('Mike', 'Brown', 'LIC123', 'Car', 'Available'),
('Sarah', 'Lee', 'LIC456', 'Bike', 'Busy');

CREATE TABLE `Order` (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    order_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) NOT NULL,
    delivery_address VARCHAR(255) NOT NULL,
    total_amount DECIMAL(10,2),
    customer_id INT NOT NULL,
    restaurant_id INT NOT NULL,
    driver_id INT,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (restaurant_id) REFERENCES Restaurant(restaurant_id),
    FOREIGN KEY (driver_id) REFERENCES Driver(driver_id)
);

INSERT INTO `Order` (status, delivery_address, total_amount, customer_id, restaurant_id, driver_id)
VALUES
('Delivered', '789 Oak St', 25.98, 1, 1, 1),
('Preparing', '321 Pine St', 17.98, 2, 2, 2);

CREATE TABLE MenuItem (
    menu_item_id INT PRIMARY KEY AUTO_INCREMENT,
    restaurant_id INT NOT NULL,
    item_name VARCHAR(150) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    description TEXT,
    availability_status VARCHAR(50) NOT NULL,
    UNIQUE (restaurant_id, item_name),
    FOREIGN KEY (restaurant_id) REFERENCES Restaurant(restaurant_id)
);

INSERT INTO MenuItem (restaurant_id, item_name, price, description, availability_status)
VALUES
(1, 'Pepperoni Pizza', 12.99, 'Large pepperoni pizza', 'Available'),
(1, 'Margherita Pizza', 10.99, 'Classic cheese pizza', 'Available'),
(2, 'California Roll', 8.99, 'Crab and avocado roll', 'Available');

CREATE TABLE OrderItem (
    order_item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    menu_item_id INT NOT NULL,
    quantity INT NOT NULL,
    subtotal DECIMAL(10,2),
    UNIQUE (order_id, menu_item_id),
    FOREIGN KEY (order_id) REFERENCES `Order`(order_id),
    FOREIGN KEY (menu_item_id) REFERENCES MenuItem(menu_item_id)
);

INSERT INTO OrderItem (order_id, menu_item_id, quantity, subtotal)
VALUES
(1, 1, 2, 25.98),
(2, 3, 2, 17.98);

CREATE TABLE Payment (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL UNIQUE,
    payment_method VARCHAR(50) NOT NULL,
    payment_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    payment_status VARCHAR(50) NOT NULL,
    transaction_reference VARCHAR(100),
    FOREIGN KEY (order_id) REFERENCES `Order`(order_id)
);

INSERT INTO Payment (order_id, payment_method, payment_status, transaction_reference)
VALUES
(1, 'Credit Card', 'Completed', 'TXN123'),
(2, 'PayPal', 'Pending', 'TXN456');

CREATE TABLE Review (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    restaurant_id INT NOT NULL,
    rating INT NOT NULL,
    comment TEXT,
    review_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (customer_id, restaurant_id),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (restaurant_id) REFERENCES Restaurant(restaurant_id)
);

INSERT INTO Review (customer_id, restaurant_id, rating, comment)
VALUES
(1, 1, 5, 'Excellent pizza!'),
(2, 2, 4, 'Fresh sushi, fast delivery!');
