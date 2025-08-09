import os
import logging
import mysql.connector
from flask import Flask, request, jsonify, send_from_directory, render_template_string
from flask_restx import Api, Resource, fields
from flask_cors import CORS
import time
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s", "module": "%(name)s"}',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Enable CORS for frontend integration
CORS(app)

# API Documentation setup
api = Api(
    app,
    version='2.0',
    title='Todo API',
    description='A simple Todo API with Docker and MySQL',
    doc='/docs/'
)

ns = api.namespace('todos', description='Todo operations')

# API Models for documentation
todo_model = api.model('Todo', {
    'task': fields.String(required=True, description='The todo task description')
})

todo_response = api.model('TodoResponse', {
    'id': fields.Integer(description='Todo ID'),
    'task': fields.String(description='Todo task description')
})

db_config = {
    'host': os.getenv('DB_HOST', 'db'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'rootpass'),
    'database': os.getenv('DB_NAME', 'todo_db'),
    'port': int(os.getenv('DB_PORT', 3306))
}

def get_db_connection():
    """Get database connection with retry logic"""
    max_retries = 5
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            conn = mysql.connector.connect(**db_config)
            logger.info(f"Database connection successful on attempt {attempt + 1}")
            return conn
        except mysql.connector.Error as e:
            logger.warning(f"Database connection attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                logger.error("All database connection attempts failed")
                raise

@app.route("/health")
def health_check():
    """Health check endpoint"""
    try:
        # Check database connectivity
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        conn.close()
        
        health_status = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "database": "connected",
            "version": "2.0"
        }
        logger.info("Health check passed")
        return jsonify(health_status), 200
        
    except Exception as e:
        health_status = {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "database": "disconnected",
            "error": str(e),
            "version": "2.0"
        }
        logger.error(f"Health check failed: {e}")
        return jsonify(health_status), 503

@ns.route("/add")
class AddTodo(Resource):
    @ns.expect(todo_model)
    @ns.marshal_with(api.model('AddResponse', {
        'message': fields.String(description='Response message'),
        'id': fields.Integer(description='Created todo ID')
    }))
    def post(self):
        """Add a new todo item"""
        try:
            data = request.json
            if not data or 'task' not in data:
                logger.warning("Invalid request data for add todo")
                return {"error": "Task is required"}, 400
            
            task = data['task'].strip()
            if not task:
                logger.warning("Empty task provided")
                return {"error": "Task cannot be empty"}, 400
            
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO todos (task, created_at) VALUES (%s, %s)", 
                         (task, datetime.utcnow()))
            todo_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            logger.info(f"Todo added successfully: ID {todo_id}, Task: {task}")
            return {"message": "Task added", "id": todo_id}, 201
            
        except Exception as e:
            logger.error(f"Error adding todo: {e}")
            return {"error": "Internal server error"}, 500

@ns.route("/list")
class ListTodos(Resource):
    @ns.marshal_list_with(todo_response)
    def get(self):
        """Get all todo items"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, task FROM todos ORDER BY created_at DESC")
            tasks = [{"id": row[0], "task": row[1]} for row in cursor.fetchall()]
            conn.close()
            
            logger.info(f"Retrieved {len(tasks)} todos")
            return tasks, 200
            
        except Exception as e:
            logger.error(f"Error retrieving todos: {e}")
            return {"error": "Internal server error"}, 500

@ns.route("/<int:todo_id>")
class TodoItem(Resource):
    def delete(self, todo_id):
        """Delete a todo item"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
            
            if cursor.rowcount == 0:
                conn.close()
                logger.warning(f"Todo not found for deletion: ID {todo_id}")
                return {"error": "Todo not found"}, 404
            
            conn.commit()
            conn.close()
            
            logger.info(f"Todo deleted successfully: ID {todo_id}")
            return {"message": "Todo deleted"}, 200
            
        except Exception as e:
            logger.error(f"Error deleting todo: {e}")
            return {"error": "Internal server error"}, 500

def init_database():
    """Initialize database with retries"""
    max_retries = 10
    retry_delay = 3
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Database initialization attempt {attempt + 1}")
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Create todos table with additional fields
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS todos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    task VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed BOOLEAN DEFAULT FALSE
                )
            """)
            
            conn.commit()
            conn.close()
            logger.info("Database initialized successfully")
            return
            
        except Exception as e:
            logger.error(f"Database initialization attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                logger.error("Failed to initialize database after all attempts")
                raise

if __name__ == "__main__":
    logger.info("Starting Todo Application v2.0")
    logger.info(f"Environment: {os.getenv('FLASK_ENV', 'production')}")
    
    # Initialize database
    init_database()
    
    # Start Flask app
    debug_mode = os.getenv('FLASK_ENV') == 'development'
    app.run(
        host="0.0.0.0", 
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=debug_mode
    )
