import csv
import os
import statistics

EXPORT_DIR = "exports"

def export_to_csv(data, filename):
    if not data:
        print(f"No data to export to {filename}")
        return

    path = os.path.join(EXPORT_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Label", "Value"])
        writer.writerows(data)

    print(f"✅ Exported data to {path}")

def print_summary_report(user_data, query_data, time_data, response_times):
    print("\n📌 Summary Report")
    print(f"- Total users logged: {len(user_data)}")
    print(f"- Total unique queries: {len(query_data)}")
    print(f"- Total active days: {len(time_data)}")
    print(f"- Most recent activity date: {time_data[-1][0] if time_data else 'N/A'}")

    if response_times:
        print(f"- Response time stats (s): min={min(response_times):.3f}, max={max(response_times):.3f}, "
              f"mean={statistics.mean(response_times):.3f}, median={statistics.median(response_times):.3f}")
    else:
        print("- No response time data available.")

def print_usage_tips():
    print("\n💡 Usage Tips:")
    print("- Use --top 5 to only show the top 5 most common entries")
    print("- Add --save to export graphs as PNGs")
    print("- Use --csv to export table data to CSV")
    print("- Combine multiple flags to compare metrics at once (e.g., --user --avg --trend)")

