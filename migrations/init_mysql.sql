CREATE DATABASE IF NOT EXISTS sepehran_flights
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
USE sepehran_flights;

CREATE TABLE IF NOT EXISTS flights (
  flight_id INT PRIMARY KEY,
  flight_number VARCHAR(50) NOT NULL,
  origin VARCHAR(10) NOT NULL,
  destination VARCHAR(10) NOT NULL,
  departure_time DATETIME NOT NULL,
  arrival_time DATETIME NOT NULL,
  duration_minutes INT,
  aircraft_type VARCHAR(50),
  seats_total INT,
  seats_available INT,
  status VARCHAR(30),
  created_at DATETIME,
  updated_at DATETIME,
  process_id VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS flight_logs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  flight_id INT,
  changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  previous_state JSON,
  new_state JSON,
  note VARCHAR(255),
  INDEX (flight_id)
);
