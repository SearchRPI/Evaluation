import sqlite3
import matplotlib.pyplot as plt

def fetch_search_counts_by_user(db_path='logs.db'):
    """Fetch number of search logs per user from the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id, COUNT(*) 
        FROM search_logs 
        GROUP BY user_id
    """)
    results = cursor.fetchall()

    conn.close()
    return results

def plot_search_counts(data):
    """Generate a bar chart from (user_id, count) data."""
    if not data:
        print("No data found.")
        return

    users, counts = zip(*data)

    plt.figure(figsize=(8, 5))
    plt.bar(users, counts)
    plt.title("Number of Searches per User")
    plt.xlabel("User ID")
    plt.ylabel("Search Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    data = fetch_search_counts_by_user()
    plot_search_counts(data)