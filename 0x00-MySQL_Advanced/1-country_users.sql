-- Create a table named 'users', with an enumerated column
CREATE TABLE IF NOT EXISTS users (
    PRIMARY KEY (id),
    id      INT                    NOT NULL AUTO_INCREMENT,
    email   VARCHAR(255)           NOT NULL UNIQUE,
    name    VARCHAR(255),
    country ENUM('US', 'CO', 'TN') NOT NULL
);
