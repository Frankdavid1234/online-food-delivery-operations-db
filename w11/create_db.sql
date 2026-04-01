-- Use this block from SYSTEM user
-- CREATE USER cop3710 IDENTIFIED BY "sp2026";
-- GRANT ALL PRIVILEGES TO cop3710;

-- Use this block from COP3710 user
CREATE SEQUENCE id_seq;
CREATE TABLE review (
    name        VARCHAR2(100) NOT NULL,
    email       VARCHAR2(100) PRIMARY KEY
);
CREATE TABLE customer (
    course_id   VARCHAR2(10) PRIMARY KEY,
    course_name VARCHAR2(100) NOT NULL
);
CREATE TABLE order (
    id          NUMBER PRIMARY KEY,
    email       VARCHAR2(100) NOT NULL,
    course_id   VARCHAR2(10) NOT NULL,
    FOREIGN KEY (email) REFERENCES review(email),
    FOREIGN KEY (course_id) REFERENCES customer(course_id)
);
CREATE TABLE payment (
    id          NUMBER PRIMARY KEY,
    course_id   VARCHAR2(10) NOT NULL,
    price       NUMBER(10, 2) NOT NULL,
    FOREIGN KEY (course_id) REFERENCES customer(course_id)
);
CREATE TABLE order_item (
    id          NUMBER PRIMARY KEY,
    course_id   VARCHAR2(10) NOT NULL,
    quantity    NUMBER NOT NULL,
    FOREIGN KEY (course_id) REFERENCES customer(course_id)
);
CREATE TABLE driver (
    course_id   VARCHAR2(10) PRIMARY KEY,
    stock       NUMBER NOT NULL,
    FOREIGN KEY (course_id) REFERENCES customer(course_id)
);
CREATE TABLE restaurant(
    course_id   VARCHAR2(10) PRIMARY KEY,
    name        VARCHAR2(100) NOT NULL,
    FOREIGN KEY (course_id) REFERENCES customer(course_id)
);

