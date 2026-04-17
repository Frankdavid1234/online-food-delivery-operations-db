
CREATE SEQUENCE id_seq;

-- =========================
-- BASE TABLES (no FKs)
-- =========================

CREATE TABLE Customer (
    customer_id     NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name      VARCHAR2(100) NOT NULL,
    last_name       VARCHAR2(100) NOT NULL,
    email           VARCHAR2(150) NOT NULL UNIQUE,
    phone           VARCHAR2(20),
    date_created    DATE DEFAULT SYSDATE NOT NULL
);

CREATE TABLE Restaurant (
    restaurant_id   NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name            VARCHAR2(150) NOT NULL,
    address         VARCHAR2(255) NOT NULL,
    phone           VARCHAR2(20) NOT NULL,
    cuisine_type    VARCHAR2(100),
    rating          NUMBER(3,2)
);

CREATE TABLE Driver (
    driver_id           NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name          VARCHAR2(100) NOT NULL,
    last_name           VARCHAR2(100) NOT NULL,
    license_number      VARCHAR2(50) NOT NULL UNIQUE,
    vehicle_type        VARCHAR2(50) NOT NULL,
    availability_status VARCHAR2(20) NOT NULL,
    CONSTRAINT chk_driver_status 
        CHECK (availability_status IN ('Available', 'Busy', 'Offline'))
);

-- =========================
-- DEPENDENT TABLES
-- =========================

CREATE TABLE MenuItem (
    menu_item_id        NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    restaurant_id       NUMBER NOT NULL,
    item_name           VARCHAR2(150) NOT NULL,
    price               NUMBER(10,2) NOT NULL,
    description         CLOB,
    availability_status VARCHAR2(20) NOT NULL,
    CONSTRAINT chk_menuitem_status 
        CHECK (availability_status IN ('Available', 'Unavailable')),
    CONSTRAINT fk_menuitem_restaurant 
        FOREIGN KEY (restaurant_id) REFERENCES Restaurant(restaurant_id)
);

CREATE TABLE Food_Order (
    order_id            NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_date          DATE DEFAULT SYSDATE NOT NULL,
    status              VARCHAR2(50) NOT NULL,
    delivery_address    VARCHAR2(255) NOT NULL,
    total_amount        NUMBER(10,2),
    customer_id         NUMBER NOT NULL,
    restaurant_id       NUMBER NOT NULL,
    driver_id           NUMBER,
    CONSTRAINT chk_order_status 
        CHECK (status IN ('Pending','Confirmed','Preparing','Out for Delivery','Delivered','Cancelled')),
    CONSTRAINT fk_order_customer 
        FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    CONSTRAINT fk_order_restaurant 
        FOREIGN KEY (restaurant_id) REFERENCES Restaurant(restaurant_id),
    CONSTRAINT fk_order_driver 
        FOREIGN KEY (driver_id) REFERENCES Driver(driver_id)
);

CREATE TABLE OrderItem (
    order_id        NUMBER NOT NULL,
    order_item_id   NUMBER GENERATED ALWAYS AS IDENTITY,
    menu_item_id    NUMBER NOT NULL,
    quantity        NUMBER NOT NULL,
    subtotal        NUMBER(10,2) NOT NULL,
    CONSTRAINT pk_orderitem 
        PRIMARY KEY (order_id, order_item_id),
    CONSTRAINT chk_orderitem_qty 
        CHECK (quantity > 0),
    CONSTRAINT fk_orderitem_order 
        FOREIGN KEY (order_id) REFERENCES Food_Order(order_id),
    CONSTRAINT fk_orderitem_menuitem 
        FOREIGN KEY (menu_item_id) REFERENCES MenuItem(menu_item_id)
);

CREATE TABLE Payment (
    payment_id              NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id                NUMBER NOT NULL UNIQUE,
    payment_method          VARCHAR2(50) NOT NULL,
    payment_date            DATE DEFAULT SYSDATE NOT NULL,
    payment_status          VARCHAR2(20) NOT NULL,
    transaction_reference   VARCHAR2(100),
    CONSTRAINT chk_payment_status 
        CHECK (payment_status IN ('Pending','Completed','Failed','Refunded')),
    CONSTRAINT fk_payment_order 
        FOREIGN KEY (order_id) REFERENCES Food_Order(order_id)
);

-- COMMENT is reserved → must be quoted
CREATE TABLE Review (
    review_id       NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id     NUMBER NOT NULL,
    restaurant_id   NUMBER NOT NULL,
    rating          NUMBER(1) NOT NULL,
    review_date     DATE DEFAULT SYSDATE NOT NULL,
    CONSTRAINT chk_review_rating 
        CHECK (rating BETWEEN 1 AND 5),
    CONSTRAINT fk_review_customer 
        FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    CONSTRAINT fk_review_restaurant 
        FOREIGN KEY (restaurant_id) REFERENCES Restaurant(restaurant_id)
);