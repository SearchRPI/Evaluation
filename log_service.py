from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_FILE = "logs.db"

# Ensure the database is set up
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS search_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_id TEXT,
                search_query TEXT
            )
        """)
        conn.commit()

@app.route('/log', methods=['POST'])
def log_search():
    """Endpoint to receive and store logs"""
    data = request.json
    user_id = data.get("user_id")
    search_query = data.get("search_query")

    if not user_id or not search_query:
        return jsonify({"error": "Missing user_id or search_query"}), 400

    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO search_logs (user_id, search_query) VALUES (?, ?)", (user_id, search_query))
        conn.commit()

    return jsonify({"message": "Log stored successfully"}), 201

@app.route('/logs', methods=['GET'])
def get_logs():
    """Retrieve stored logs"""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM search_logs ORDER BY timestamp DESC")
        logs = cursor.fetchall()

    return jsonify(logs), 200

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
