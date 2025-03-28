import sqlite3

conn = sqlite3.connect("logs.db")
cursor = conn.cursor()

# Delete all rows from the search_logs table
cursor.execute("DELETE FROM search_logs")

conn.commit()
conn.close()
print("logs.db has been cleared.")
