
CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    theme int,
    temperatureUnit  char(1)
);

CREATE TABLE dashboard (
    id INT PRIMARY KEY,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE location (
    location VARCHAR(50) PRIMARY KEY
);

CREATE TABLE dashboard_locations (
    dashboard_id INT NOT NULL,
    location_id INT NOT NULL,
    PRIMARY KEY (dashboard_id, location_id),
    FOREIGN KEY (dashboard_id) REFERENCES dashboard(id),
    FOREIGN KEY (location_id) REFERENCES location(id)
);

CREATE TABLE dashboard_shares (
    dashboard_id INT NOT NULL,
    user_id INT NOT NULL,
    PRIMARY KEY (dashboard_id, user_id),
    FOREIGN KEY (dashboard_id) REFERENCES dashboard(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);
