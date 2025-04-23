import sqlite3
import csv
import argparse
import os

def import_from_csv(csv_file, db_file='logs.db'):
    if not os.path.exists(csv_file):
        print(f"File not found: {csv_file}")
        return

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS search_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            user_id TEXT,
            search_query TEXT,
            response_time REAL
        )
    """)

    with open(csv_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            cursor.execute("""
                INSERT INTO search_logs (timestamp, user_id, search_query, response_time)
                VALUES (?, ?, ?, ?)
            """, (row['timestamp'], row['user_id'], row['search_query'], float(row['response_time'])))
            count += 1

    conn.commit()
    conn.close()
    print(f"Imported {count} log entries into {db_file}")

def main():
    parser = argparse.ArgumentParser(description="Import search logs from a CSV file into logs.db")
    parser.add_argument("csv_file", help="Path to the CSV file to import")
    parser.add_argument("--db", default="logs.db", help="Target SQLite database file")
    args = parser.parse_args()

    import_from_csv(args.csv_file, db_file=args.db)

if __name__ == "__main__":
    main()
