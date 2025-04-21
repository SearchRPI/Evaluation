import argparse
from utils.db_utils import fetch_data
from utils.stats_utils import compute_summary_stats, print_summary_report

def main():
    parser = argparse.ArgumentParser(description="Quickly summarize logs.db search data")
    parser.add_argument("--db", type=str, default="logs.db", help="Path to SQLite database")
    args = parser.parse_args()

    print("\n🔍 Running log_stats on:", args.db)

    user_data, query_data, time_data, avg_data, hour_data, response_times = fetch_data(args.db)
    stats = compute_summary_stats(user_data, query_data, time_data, hour_data, response_times)

    print_summary_report(stats)
    print("\n✅ Done.")

if __name__ == "__main__":
    main()
