from flask import Flask, render_template, send_from_directory
import os
from log_visualizer import fetch_data, plot_bar_chart, plot_line_chart

app = Flask(__name__)
EXPORT_FOLDER = "web_exports"

# Ensure export folder exists
os.makedirs(EXPORT_FOLDER, exist_ok=True)

@app.route("/")
def index():
    # Generate charts and save to PNG files
    user_data, query_data, time_data, avg_data = fetch_data()

    plot_bar_chart(user_data, "Searches Per User", "User ID", "Search Count", save=True)
    plot_bar_chart(query_data, "Searches Per Query", "Search Query", "Count", save=True)
    plot_bar_chart(time_data, "Searches Per Day", "Date", "Count", save=True)
    plot_line_chart(time_data, "Searches Per Day (Line Chart)", "Date", "Count", save=True)
    plot_bar_chart(avg_data, "Average Response Time Per User", "User ID", "Avg Response Time (s)", save=True)

    # Move images to export folder (if not already saved there)
    filenames = [
        "searches_per_user.png",
        "searches_per_query.png",
        "searches_per_day.png",
        "searches_per_day_(line_chart).png",
        "average_response_time_per_user.png"
    ]

    for f in filenames:
        if os.path.exists(f):
            os.replace(f, os.path.join(EXPORT_FOLDER, f))

    return render_template("index.html", images=filenames)

@app.route("/charts/<filename>")
def charts(filename):
    return send_from_directory(EXPORT_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)