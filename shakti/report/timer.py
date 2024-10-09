import re
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from july import heatmap
from july.utils import date_range
from matplotlib.backends.backend_pdf import PdfPages
import os
import warnings


def parse_timer_file(file_path):
    data = {}
    with open(file_path, "r") as f:
        for line in f:
            match = re.match(
                r"\[(\d{4}-\d{2}-\d{2}) .*?\] = \[(\d{2}):(\d{2}):(\d{2})\]", line
            )
            if match:
                date, hours, minutes, seconds = match.groups()
                duration = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
                data[date] = data.get(date, 0) + duration
    return data


def create_heatmap(data):
    dates = date_range(min(data.keys()), max(data.keys()))
    values = [
        data.get(date.strftime("%Y-%m-%d"), 0) / 3600 for date in dates
    ]  # Convert seconds to hours

    # Suppress all warnings
    warnings.filterwarnings("ignore")

    fig, ax = plt.subplots(figsize=(12, 8))
    heatmap(dates, values, title="Work Activity Heatmap", cmap="github", ax=ax)
    plt.tight_layout()
    return fig


def main(timer_file_path):
    if not os.path.exists(timer_file_path):
        print(f"Error: {timer_file_path} not found.")
        return

    data = parse_timer_file(timer_file_path)
    fig = create_heatmap(data)

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "work_activity_heatmap.pdf")

    with PdfPages(output_path) as pdf:
        pdf.savefig(fig)

    print(f"Heatmap saved as: {os.path.abspath(output_path)}")


if __name__ == "__main__":
    main(".timer")
