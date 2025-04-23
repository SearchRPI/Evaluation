import os
from log_visualizer import fetch_data, export_to_csv, print_summary_report

MENU = """
SearchRPI Log CLI
------------------
1. View summary report
2. Export data to CSV
3. Exit
"""

def cli_loop():
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()

        if choice == "1":
            user_data, query_data, time_data, avg_data, hour_data, response_times = fetch_data()
            print_summary_report({
                "total_logs": sum([count for _, count in time_data]),
                "total_users": len(user_data),
                "total_queries": len(query_data),
                "active_days": len(time_data),
                "peak_hour": max(hour_data, key=lambda x: x[1])[0] if hour_data else None,
                "most_active_user": max(user_data, key=lambda x: x[1])[0] if user_data else None,
                "top_query": max(query_data, key=lambda x: x[1])[0] if query_data else None,
                "fastest_response": min(response_times) if response_times else None,
                "slowest_response": max(response_times) if response_times else None,
                "mean_response": sum(response_times) / len(response_times) if response_times else None
            })

        elif choice == "2":
            filename = input("Enter CSV filename: ").strip()
            user_data, _, _, _, _, _ = fetch_data()
            export_to_csv(user_data, filename)

        elif choice == "3":
            print("Exiting CLI...")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    cli_loop()
