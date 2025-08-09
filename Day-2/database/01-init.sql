-- Database initialization script
-- This script runs automatically when MySQL container starts

USE todo_db;

-- Create todos table with enhanced structure
CREATE TABLE IF NOT EXISTS todos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    completed BOOLEAN DEFAULT FALSE,
    priority ENUM('low', 'medium', 'high') DEFAULT 'medium',
    INDEX idx_created_at (created_at),
    INDEX idx_completed (completed)
);

-- Create logs table for application logging (optional)
CREATE TABLE IF NOT EXISTS app_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    level VARCHAR(20),
    message TEXT,
    module_name VARCHAR(100),
    INDEX idx_timestamp (timestamp),
    INDEX idx_level (level)
);
