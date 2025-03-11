from flask import Flask, request, jsonify
import sqlite3

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
                user_id TEXT NOT NULL,
                search_query TEXT NOT NULL,
                response_time REAL
            )
        """)
        conn.commit()

@app.route('/log', methods=['POST'])
def log_search():
    """Endpoint to receive and store logs"""
    data = request.json

    # Validate required fields
    if not data or "user_id" not in data or "search_query" not in data:
        return jsonify({"error": "Missing required fields: user_id, search_query"}), 400

    user_id = data["user_id"]
    search_query = data["search_query"]
    response_time = data.get("response_time")  # Optional

    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO search_logs (user_id, search_query, response_time) 
            VALUES (?, ?, ?)
        """, (user_id, search_query, response_time))
        conn.commit()

    return jsonify({"message": "Log stored successfully"}), 201

@app.route('/logs', methods=['GET'])
def get_logs():
    """Retrieve stored logs, with optional filtering by user_id and timestamp"""
    user_id = request.args.get("user_id")
    start_time = request.args.get("start_time")  # Optional filter by timestamp
    end_time = request.args.get("end_time")

    query = "SELECT * FROM search_logs WHERE 1=1"
    params = []

    if user_id:
        query += " AND user_id = ?"
        params.append(user_id)
    if start_time:
        query += " AND timestamp >= ?"
        params.append(start_time)
    if end_time:
        query += " AND timestamp <= ?"
        params.append(end_time)

    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        logs = cursor.fetchall()

    return jsonify(logs), 200

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
