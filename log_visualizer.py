import argparse
import os
import textwrap
from utils.db_utils import fetch_data
from utils.plot_utils import plot_bar_chart, plot_line_chart
from utils.export_utils import export_to_csv, print_summary_report, print_usage_tips

# Default database path
DEFAULT_DB = 'logs.db'

# Create an output folder for saving files
EXPORT_DIR = "exports"
os.makedirs(EXPORT_DIR, exist_ok=True)

BANNER = textwrap.dedent("""
    ==========================================
    |        SEARCH LOG VISUALIZER TOOL       |
    ==========================================
""")


if __name__ == "__main__":
    print(BANNER)
    parser = argparse.ArgumentParser(description="Visualize search logs from logs.db")
    parser.add_argument("--user", action="store_true", help="Show search count per user")
    parser.add_argument("--query", action="store_true", help="Show search count per query")
    parser.add_argument("--time", action="store_true", help="Show search count per day")
    parser.add_argument("--hour", action="store_true", help="Show search volume by hour of day")
    parser.add_argument("--avg", action="store_true", help="Show average response time per user")
    parser.add_argument("--trend", action="store_true", help="Show time-series line chart of searches per day")
    parser.add_argument("--save", action="store_true", help="Save graphs as PNG instead of showing them")
    parser.add_argument("--csv", action="store_true", help="Export selected data to CSV")
    parser.add_argument("--top", type=int, help="Only show top N results in graphs")
    parser.add_argument("--db", type=str, default=DEFAULT_DB, help="Specify an alternate database path")

    args = parser.parse_args()
    print("📊Log Visualizer starting with options:")
    for arg, val in vars(args).items():
        print(f"  --{arg}: {val}")

    user_data, query_data, time_data, avg_data, hour_data, response_times = fetch_data(args.db)

    if args.user:
        plot_bar_chart(user_data, "Searches Per User", "User ID", "Search Count", save=args.save, top_n=args.top)
        if args.csv:
            export_to_csv(user_data, "searches_per_user.csv")

    if args.query:
        plot_bar_chart(query_data, "Searches Per Query", "Search Query", "Count", save=args.save, top_n=args.top)
        if args.csv:
            export_to_csv(query_data, "searches_per_query.csv")

    if args.time:
        plot_bar_chart(time_data, "Searches Per Day", "Date", "Count", save=args.save, top_n=args.top)
        if args.csv:
            export_to_csv(time_data, "searches_per_day.csv")

    if args.hour:
        plot_bar_chart(hour_data, "Searches by Hour of Day", "Hour", "Count", save=args.save, top_n=args.top)
        if args.csv:
            export_to_csv(hour_data, "searches_per_hour.csv")

    if args.avg:
        plot_bar_chart(avg_data, "Average Response Time Per User", "User ID", "Avg Response Time (s)", save=args.save, top_n=args.top)
        if args.csv:
            export_to_csv(avg_data, "avg_response_time.csv")

    if args.trend:
        plot_line_chart(time_data, "Searches Per Day (Line Chart)", "Date", "Count", save=args.save)
        if args.csv:
            export_to_csv(time_data, "searches_per_day.csv")

    if not any([args.user, args.query, args.time, args.avg, args.trend, args.hour]):
        plot_bar_chart(user_data, "Searches Per User", "User ID", "Search Count", save=args.save, top_n=args.top)
        plot_bar_chart(query_data, "Searches Per Query", "Search Query", "Count", save=args.save, top_n=args.top)
        plot_bar_chart(time_data, "Searches Per Day", "Date", "Count", save=args.save, top_n=args.top)
        plot_bar_chart(avg_data, "Average Response Time Per User", "User ID", "Avg Response Time (s)", save=args.save, top_n=args.top)
        plot_bar_chart(hour_data, "Searches by Hour of Day", "Hour", "Search Count", save=args.save, top_n=args.top)
        plot_line_chart(time_data, "Searches Per Day", "Date", "Count", save=args.save)

    print_summary_report(user_data, query_data, time_data, response_times)
    print_usage_tips()
    print("Visualization complete!")
