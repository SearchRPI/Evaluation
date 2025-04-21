import argparse
import sqlite3
import csv
from datetime import datetime

def filter_logs(db_path, user=None, query=None, start=None, end=None, flagged=None, only_flagged=False):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    sql = "SELECT timestamp, user_id, search_query, response_time FROM search_logs WHERE 1=1"
    params = []

    if user:
        sql += " AND user_id = ?"
        params.append(user)
    if query:
        sql += " AND search_query LIKE ?"
        params.append(f"%{query}%")
    if start:
        sql += " AND timestamp >= ?"
        params.append(start)
    if end:
        sql += " AND timestamp <= ?"
        params.append(end)

    cursor.execute(sql, params)
    results = cursor.fetchall()
    conn.close()

    if flagged:
        results = [r for r in results if flagged.lower() in r[2].lower() or not only_flagged]
        if only_flagged:
            results = [r for r in results if flagged.lower() in r[2].lower()]

    return results

def print_logs(logs, flagged=None):
    print("\n📄 Filtered Logs:")
    if not logs:
        print("No logs match the given criteria.")
        return

    for timestamp, user_id, query, resp_time in logs:
        flag = " 🚩" if flagged and flagged.lower() in query.lower() else ""
        print(f"[{timestamp}] user='{user_id}' query='{query}' time={resp_time:.3f}s{flag}")

def export_logs_to_csv(logs, filename):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "user_id", "search_query", "response_time"])
        writer.writerows(logs)
    print(f"\n✅ Exported {len(logs)} logs to '{filename}'")

def main():
    parser = argparse.ArgumentParser(description="Filter and view logs from logs.db")
    parser.add_argument("--db", type=str, default="logs.db", help="Path to SQLite database")
    parser.add_argument("--user", help="Filter by user ID")
    parser.add_argument("--query", help="Search by query keyword")
    parser.add_argument("--start", help="Start timestamp (YYYY-MM-DD or full ISO format)")
    parser.add_argument("--end", help="End timestamp (YYYY-MM-DD or full ISO format)")
    parser.add_argument("--flagged", help="Flag specific search terms of interest")
    parser.add_argument("--only-flagged", action="store_true", help="Only show logs that include flagged terms")
    parser.add_argument("--export", type=str, help="Export filtered logs to a CSV file")

    args = parser.parse_args()

    logs = filter_logs(
        db_path=args.db,
        user=args.user,
        query=args.query,
        start=args.start,
        end=args.end,
        flagged=args.flagged,
        only_flagged=args.only_flagged
    )

    print_logs(logs, flagged=args.flagged)

    if args.export:
        export_logs_to_csv(logs, args.export)

if __name__ == "__main__":
    main()
