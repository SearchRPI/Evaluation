import sqlite3
import argparse
import time

INDEXES = [
    ("idx_timestamp", "timestamp"),
    ("idx_user_id", "user_id"),
    ("idx_search_query", "search_query")
]

def add_indexes(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    for idx_name, col in INDEXES:
        print(f"Adding index on '{col}'...")
        try:
            cursor.execute(f"CREATE INDEX IF NOT EXISTS {idx_name} ON search_logs({col})")
        except Exception as e:
            print(f"Failed to add index {idx_name}: {e}")
    conn.commit()
    conn.close()
    print("Index optimization complete.")

def benchmark_query(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    print("\n⏱Benchmarking common queries:")

    start = time.time()
    cursor.execute("SELECT COUNT(*) FROM search_logs")
    print("Total entries:", cursor.fetchone()[0])
    print("Query 1 time:", round(time.time() - start, 4), "s")

    start = time.time()
    cursor.execute("SELECT COUNT(*) FROM search_logs WHERE user_id = 'test_user_1'")
    print("Query 2 time:", round(time.time() - start, 4), "s")

    start = time.time()
    cursor.execute("SELECT COUNT(*) FROM search_logs WHERE search_query LIKE '%flask%'")
    print("Query 3 time:", round(time.time() - start, 4), "s")

    conn.close()

def main():
    parser = argparse.ArgumentParser(description="Add indexes to logs.db for query performance optimization")
    parser.add_argument("--db", default="logs.db", help="Path to the SQLite database")
    parser.add_argument("--benchmark", action="store_true", help="Run benchmark queries before and after")
    args = parser.parse_args()

    if args.benchmark:
        print("\nBEFORE INDEXES:")
        benchmark_query(args.db)

    add_indexes(args.db)

    if args.benchmark:
        print("\nAFTER INDEXES:")
        benchmark_query(args.db)

if __name__ == "__main__":
    main()
