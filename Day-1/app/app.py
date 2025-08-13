import os
import time
import mysql.connector
from mysql.connector import Error
from flask import Flask, request, jsonify

app = Flask(__name__)

db_config = {
    'host': os.getenv('DB_HOST', 'db'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'rootpass'),
    'database': os.getenv('DB_NAME', 'todo_db')
}

def wait_for_db(max_retries=10, delay=3):
    """Wait until the MySQL database is ready."""
    for attempt in range(1, max_retries + 1):
        try:
            conn = mysql.connector.connect(**db_config)
            if conn.is_connected():
                print("✅ Connected to MySQL!")
                conn.close()
                return True
        except Error as e:
            print(f"⏳ Waiting for MySQL... attempt {attempt}/{max_retries} - {e}")
            time.sleep(delay)
    print("❌ Could not connect to MySQL after retries.")
    return False

@app.route("/add", methods=["POST"])
def add_todo():
    data = request.json
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todos (task) VALUES (%s)", (data["task"],))
    conn.commit()
    conn.close()
    return jsonify({"message": "Task added"}), 201

@app.route("/list", methods=["GET"])
def list_todos():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todos")
    tasks = [{"id": row[0], "task": row[1]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(tasks)

if __name__ == "__main__":
    if wait_for_db():
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                task VARCHAR(255)
            )
        """)
        conn.commit()
        conn.close()
        app.run(host="0.0.0.0", port=5000)
    else:
        print("❌ MySQL not available. Exiting.")
