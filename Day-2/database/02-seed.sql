-- Sample data for testing
-- This script runs after initialization

USE todo_db;

-- Insert sample todos
INSERT INTO todos (task, priority, completed) VALUES 
('Learn Docker fundamentals', 'high', true),
('Set up Docker Compose', 'high', true),
('Implement health checks', 'medium', false),
('Add API documentation', 'medium', false),
('Configure environment variables', 'high', false),
('Set up logging', 'low', false),
('Create multi-stage builds', 'medium', false),
('Deploy to production', 'high', false);

-- Insert a welcome log entry
INSERT INTO app_logs (level, message, module_name) VALUES 
('INFO', 'Database initialized with sample data', 'init_script');
