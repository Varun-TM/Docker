import os
import mysql.connector
from flask import Flask, request, jsonify

app = Flask(__name__)

db_config = {
    'host': os.getenv('DB_HOST', 'db'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'rootpass'),
    'database': os.getenv('DB_NAME', 'todo_db')
}

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
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS todos (id INT AUTO_INCREMENT PRIMARY KEY, task VARCHAR(255))")
    conn.commit()
    conn.close()
    app.run(host="0.0.0.0", port=5000)

