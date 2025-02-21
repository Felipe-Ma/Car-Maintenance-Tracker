-- Create the database (if it doesn't exist)
CREATE DATABASE IF NOT EXISTS car_maintenance;
USE car_maintenance;

-- Create the cars table
CREATE TABLE IF NOT EXISTS cars (
    id INT AUTO_INCREMENT PRIMARY KEY,
    make VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    year INT NOT NULL,
    vin VARCHAR(20) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the service_types table
CREATE TABLE IF NOT EXISTS service_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Insert default service types
INSERT IGNORE INTO service_types (name) VALUES
('Oil Change'),
('Tire Rotation'),
('Brake Inspection'),
('Battery Replacement'),
('General Checkup');

-- Create the maintenance_records table
CREATE TABLE IF NOT EXISTS maintenance_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    car_id INT NOT NULL,
    service_type_id INT NOT NULL,
    service_date DATE NOT NULL,
    mileage INT NOT NULL,
    cost DECIMAL(10,2) NULL,
    notes TEXT,
    next_due_mileage INT NULL,
    FOREIGN KEY (car_id) REFERENCES cars(id) ON DELETE CASCADE,
    FOREIGN KEY (service_type_id) REFERENCES service_types(id) ON DELETE CASCADE
);
