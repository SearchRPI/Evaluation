import matplotlib.pyplot as plt
import os
from datetime import datetime

EXPORT_DIR = "exports"

def plot_bar_chart(data, title, xlabel, ylabel, save=False, top_n=None):
    if not data:
        print(f"No data to plot for {title}")
        return

    data = sorted(data, key=lambda x: x[1], reverse=True)
    if top_n:
        data = data[:top_n]

    labels, values = zip(*data)
    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color="skyblue")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()

    if save:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(EXPORT_DIR, title.lower().replace(" ", "_") + f"_{timestamp}.png")
        plt.savefig(filename)
        print(f"📁 Saved graph to {filename}")
    else:
        plt.show()

def plot_line_chart(data, title, xlabel, ylabel, save=False):
    if not data:
        print(f"No data to plot for {title}")
        return

    data = sorted(data, key=lambda x: x[0])
    dates, counts = zip(*data)
    plt.figure(figsize=(10, 6))
    plt.plot(dates, counts, marker='o', linestyle='-', color='darkgreen')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()

    if save:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(EXPORT_DIR, title.lower().replace(" ", "_") + f"_{timestamp}.png")
        plt.savefig(filename)
        print(f"📁 Saved graph to {filename}")
    else:
        plt.show()
