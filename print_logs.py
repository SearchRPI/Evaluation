import sqlite3

# Connect to the logs database
conn = sqlite3.connect("logs.db")
cursor = conn.cursor()

# Fetch all logs
cursor.execute("SELECT * FROM search_logs ORDER BY timestamp DESC")
logs = cursor.fetchall()

# Print them nicely
for log in logs:
    print(log)

conn.close()
