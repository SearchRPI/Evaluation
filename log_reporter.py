import sqlite3
from datetime import datetime

def generate_report(db_path='logs.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("\nLog System Summary Report")
    print("-------------------------")

    cursor.execute("SELECT COUNT(*) FROM search_logs")
    total_logs = cursor.fetchone()[0]
    print(f"Total logs: {total_logs}")

    cursor.execute("SELECT COUNT(DISTINCT user_id) FROM search_logs")
    total_users = cursor.fetchone()[0]
    print(f"Total unique users: {total_users}")

    cursor.execute("SELECT COUNT(DISTINCT search_query) FROM search_logs")
    total_queries = cursor.fetchone()[0]
    print(f"Total unique queries: {total_queries}")

    cursor.execute("SELECT MIN(timestamp), MAX(timestamp) FROM search_logs")
    start, end = cursor.fetchone()
    print(f"Time range: {start} to {end}")

    cursor.execute("SELECT AVG(response_time), MIN(response_time), MAX(response_time) FROM search_logs")
    avg_rt, min_rt, max_rt = cursor.fetchone()
    print(f"Avg response time: {avg_rt:.3f}s")
    print(f"Min response time: {min_rt:.3f}s")
    print(f"Max response time: {max_rt:.3f}s")

    cursor.execute("SELECT user_id, COUNT(*) as c FROM search_logs GROUP BY user_id ORDER BY c DESC LIMIT 1")
    top_user = cursor.fetchone()
    print(f"Most active user: {top_user[0]} with {top_user[1]} searches")

    cursor.execute("SELECT search_query, COUNT(*) as c FROM search_logs GROUP BY search_query ORDER BY c DESC LIMIT 1")
    top_query = cursor.fetchone()
    print(f"Most common query: '{top_query[0]}' ({top_query[1]} times)")

    conn.close()

def main():
    generate_report()

if __name__ == "__main__":
    main()
