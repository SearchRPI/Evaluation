import sqlite3
from datetime import datetime, timedelta
import random

# Connect to your logs database
conn = sqlite3.connect("logs.db")
cursor = conn.cursor()

# List of fake users and queries
users = ["test_user_1", "test_user_2", "test_user_3"]
queries = [
    "how to use flask",
    "searchRPI logging",
    "best pizza in nyc",
    "debug python service",
    "visualize sqlite data"
]

# Generate 20 fake logs
for _ in range(20):
    user_id = random.choice(users)
    search_query = random.choice(queries)
    response_time = round(random.uniform(0.1, 1.0), 3)

    # Random timestamp in the last 7 days
    timestamp = datetime.now() - timedelta(days=random.randint(0, 6), hours=random.randint(0, 23))
    timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO search_logs (timestamp, user_id, search_query, response_time)
        VALUES (?, ?, ?, ?)
    """, (timestamp_str, user_id, search_query, response_time))

conn.commit()
conn.close()
print("Inserted 20 fake log entries into logs.db.")