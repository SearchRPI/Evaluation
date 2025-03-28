import sqlite3
import matplotlib.pyplot as plt
import argparse

def fetch_data(db_path='logs.db'):
    """Fetch number of search logs per user from the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Searches per user
    cursor.execute("SELECT user_id, COUNT(*) FROM search_logs GROUP BY user_id")
    user_counts = cursor.fetchall()

    # Searches per query
    cursor.execute("SELECT search_query, COUNT(*) FROM search_logs GROUP BY search_query")
    query_counts = cursor.fetchall()

    # Searches over time
    cursor.execute("SELECT DATE(timestamp), COUNT(*) FROM search_logs GROUP BY DATE(timestamp)")
    time_counts = cursor.fetchall()

    conn.close()
    return user_counts, query_counts, time_counts

def plot_bar_chart(data, title, xlabel, ylabel, save=False):
    if not data:
        print(f"No data to plot for {title}")
        return

    # Sort by count descending
    data = sorted(data, key=lambda x: x[1], reverse=True)

    labels, values = zip(*data)
    plt.figure(figsize=(8, 5))
    plt.bar(labels, values)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()

    if save:
        filename = title.lower().replace(" ", "_") + ".png"
        plt.savefig(filename)
        print(f"Saved graph to {filename}")
    else:
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize search logs from logs.db")
    parser.add_argument("--user", action="store_true", help="Show search count per user")
    parser.add_argument("--query", action="store_true", help="Show search count per query")
    parser.add_argument("--time", action="store_true", help="Show search count per day")
    parser.add_argument("--save", action="store_true", help="Save graphs as PNG instead of showing them")

    args = parser.parse_args()

    user_data, query_data, time_data = fetch_data()

    if args.user:
        plot_bar_chart(user_data, "Searches Per User", "User ID", "Search Count", save=args.save)
    if args.query:
        plot_bar_chart(query_data, "Searches Per Query", "Search Query", "Count", save=args.save)
    if args.time:
        plot_bar_chart(time_data, "Searches Per Day", "Date", "Count", save=args.save)

    # If no options passed, show all by default
    if not any([args.user, args.query, args.time]):
        plot_bar_chart(user_data, "Searches Per User", "User ID", "Search Count", save=args.save)
        plot_bar_chart(query_data, "Searches Per Query", "Search Query", "Count", save=args.save)
        plot_bar_chart(time_data, "Searches Per Day", "Date", "Count", save=args.save)
