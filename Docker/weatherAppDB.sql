CREATE DATABASE IF NOT EXISTS weather_app_DB;
USE weather_app_DB;

-- Drop existing tables if they exist
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS dashboard_locations;
DROP TABLE IF EXISTS location;
DROP TABLE IF EXISTS user;
SET FOREIGN_KEY_CHECKS = 1;

-- Create the user table
CREATE TABLE user (
  id INT AUTO_INCREMENT, -- userid can also be interpreted as dashboardid as each user only has 1 dashboard.
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL,
  theme INT, 
  temperatureUnit ENUM('C', 'F') NOT NULL DEFAULT 'C',
  password VARCHAR(255) NOT NULL,
  PRIMARY KEY (id)
) ENGINE = InnoDB;

-- Create the location table
CREATE TABLE location (
  id INT AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  PRIMARY KEY (id)
) ENGINE = InnoDB;

-- Create the dashboard_locations table with foreign keys to user and location tables
CREATE TABLE dashboard_locations (
  user_id INT NOT NULL,  -- references the user directly
  location_id INT NOT NULL,  -- references the location
  PRIMARY KEY (user_id, location_id),
  CONSTRAINT FK_dashloc_user FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
  CONSTRAINT FK_dashloc_loc FOREIGN KEY (location_id) REFERENCES location(id) ON DELETE CASCADE
) ENGINE = InnoDB;

-- Grant all privileges on the database to testuser
GRANT ALL PRIVILEGES ON weather_app_DB.* TO 'testuser';
FLUSH PRIVILEGES;

-- ------------------------------------------------------------------------------------------------

-- Insert users (4 users with new names)
INSERT INTO user (name, email, theme, temperatureUnit, password)
VALUES
  ('Ryan Reynolds', 'ryan.reynolds@example.com', 1, 'C', 'ryanPass'),
  ('Hugh Jackman', 'hugh.jackman@example.com', 2, 'F', 'hughPass'),
  ('Chris Evans', 'chris.evans@example.com', 1, 'C', 'chrisPass'),
  ('Robert Downey Jr.', 'robert.downey@example.com', 2, 'F', 'robertPass');

-- Insert locations (10 unique locations)
INSERT INTO location (name)
VALUES
  ('New York'),
  ('Los Angeles'),
  ('Chicago'),
  ('Miami'),
  ('San Francisco'),
  ('London'),
  ('Paris'),
  ('Tokyo'),
  ('Berlin'),
  ('Sydney');

-- Insert dashboard-location relationships (user_id and location_id mappings)

-- Ryan Reynolds' dashboard is linked to 5 locations
INSERT INTO dashboard_locations (user_id, location_id)
VALUES
  (1, 1),  -- Ryan's location 1: New York
  (1, 2),  -- Ryan's location 2: Los Angeles
  (1, 3),  -- Ryan's location 3: Chicago
  (1, 4),  -- Ryan's location 4: Miami
  (1, 5);  -- Ryan's location 5: San Francisco

-- Hugh Jackman's dashboard is linked to 5 locations (3 of the same as Ryan's)
INSERT INTO dashboard_locations (user_id, location_id)
VALUES
  (2, 1),  -- Hugh's location 1 (same as Ryan): New York
  (2, 2),  -- Hugh's location 2 (same as Ryan): Los Angeles
  (2, 7),  -- Hugh's location 3: Paris
  (2, 6),  -- Hugh's location 4: London
  (2, 3);  -- Hugh's location 5 (same as Ryan): Chicago

-- Chris Evans' dashboard is linked to 5 locations (some shared with Ryan and Hugh)
INSERT INTO dashboard_locations (user_id, location_id)
VALUES
  (3, 9),  -- Chris' location 1: Berlin
  (3, 8),  -- Chris' location 2: Tokyo
  (3, 2),  -- Chris' location 3 (same as Ryan and Hugh): Los Angeles
  (3, 4),  -- Chris' location 4 (same as Ryan): Miami
  (3, 5);  -- Chris' location 5 (same as Ryan): San Francisco

-- Robert Downey Jr.'s dashboard is linked to 5 locations (some shared with others)
INSERT INTO dashboard_locations (user_id, location_id)
VALUES
  (4, 10), -- Robert's location 1: Sydney
  (4, 1),  -- Robert's location 2 (same as Ryan and Hugh): New York
  (4, 7),  -- Robert's location 3 (same as Hugh): Paris
  (4, 8),  -- Robert's location 4 (same as Chris): Tokyo
  (4, 6);  -- Robert's location 5 (same as Hugh): London
