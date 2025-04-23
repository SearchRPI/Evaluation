import time
import sqlite3
import argparse
import statistics

def benchmark_queries(db_path='logs.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    tests = [
        ("Total logs", "SELECT COUNT(*) FROM search_logs"),
        ("Searches by test_user_1", "SELECT * FROM search_logs WHERE user_id = 'test_user_1'"),
        ("Queries containing 'flask'", "SELECT * FROM search_logs WHERE search_query LIKE '%flask%'"),
        ("Response time avg", "SELECT AVG(response_time) FROM search_logs")
    ]

    times = []

    print("Benchmarking queries:")
    for label, query in tests:
        start = time.time()
        cursor.execute(query)
        cursor.fetchall()
        elapsed = round(time.time() - start, 4)
        print(f"{label}: {elapsed} seconds")
        times.append(elapsed)

    conn.close()

    print("\nStats:")
    print(f"Min time: {min(times)}s")
    print(f"Max time: {max(times)}s")
    print(f"Mean time: {statistics.mean(times):.4f}s")
    print(f"Median time: {statistics.median(times):.4f}s")

def main():
    parser = argparse.ArgumentParser(description="Run performance benchmarks on logs.db")
    parser.add_argument("--db", default="logs.db", help="Path to SQLite database")
    args = parser.parse_args()

    benchmark_queries(args.db)

if __name__ == "__main__":
    main()
