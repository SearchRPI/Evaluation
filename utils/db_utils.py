import sqlite3

def fetch_data(db_path='logs.db'):
    """Fetch various aggregate stats from the logs database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT user_id, COUNT(*) FROM search_logs GROUP BY user_id")
    user_counts = cursor.fetchall()

    cursor.execute("SELECT search_query, COUNT(*) FROM search_logs GROUP BY search_query")
    query_counts = cursor.fetchall()

    cursor.execute("SELECT DATE(timestamp), COUNT(*) FROM search_logs GROUP BY DATE(timestamp)")
    time_counts = cursor.fetchall()

    cursor.execute("SELECT user_id, AVG(response_time) FROM search_logs GROUP BY user_id")
    avg_response_times = cursor.fetchall()

    cursor.execute("SELECT strftime('%H', timestamp), COUNT(*) FROM search_logs GROUP BY strftime('%H', timestamp)")
    hour_counts = cursor.fetchall()

    cursor.execute("SELECT response_time FROM search_logs")
    response_times = [row[0] for row in cursor.fetchall()]

    conn.close()
    return user_counts, query_counts, time_counts, avg_response_times, hour_counts, response_times