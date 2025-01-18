import time
import win32gui
import win32process
import psutil
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel
from datetime import datetime, timedelta
from collections import defaultdict
import csv
import os
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import io


class ScreenTimeTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Time Tracker")
        self.root.config(bg="#4a4a4a")  # Set background color of the window
        # Calculate position for centering the window
        # Get screen width and height to center the window
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = 600
        window_height = 500

        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        # GUI Components
        self.current_app_label = ttk.Label(self.root, text="Current App: None", font=("Arial", 14), background="#4a4a4a", foreground="white")
        self.current_app_label.pack(pady=10)

        self.total_time_label = ttk.Label(self.root, text="Total Screen Time: 0 mins", font=("Arial", 12), background="#4a4a4a", foreground="white")
        self.total_time_label.pack(pady=5)

        self.tree = ttk.Treeview(self.root, columns=("App", "Total Time (mins)"), show="headings", height=15)
        self.tree.heading("App", text="App")
        self.tree.heading("Total Time (mins)", text="Total Time (mins)")
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        self.export_button = ttk.Button(self.root, text="Export Log", command=self.export_log)
        self.export_button.pack(pady=5)

        self.view_button = ttk.Button(self.root, text="View Last Day's Data", command=self.view_last_day_data)
        self.view_button.pack(pady=5)

        # Data Structures
        self.current_app = None
        self.start_time = time.time()
        self.total_time_per_app = defaultdict(float)
        self.usage_sessions = defaultdict(list)
        self.switch_counter = 0  # Count app switches
        self.running = True

        # Start tracking in a background thread
        threading.Thread(target=self.track_screen_time, daemon=True).start()

    def get_active_window_exe(self):
        """Fetch the executable name of the currently active window."""
        try:
            hwnd = win32gui.GetForegroundWindow()
            if hwnd == 0:
                return "Unknown"
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)
            return process.name().replace('.exe', '')  # Remove .exe from the name
        except Exception:
            return "Unknown"

    def track_screen_time(self):
        """Tracks screen time for each application in the background."""
        while self.running:
            active_app = self.get_active_window_exe()

            if active_app != self.current_app:
                if self.current_app:
                    # Log session details for the previous app
                    end_time = time.time()
                    duration = end_time - self.start_time
                    self.total_time_per_app[self.current_app] += duration
                    self.usage_sessions[self.current_app].append({
                        "start": datetime.fromtimestamp(self.start_time).strftime("%Y-%m-%d %H:%M:%S"),
                        "end": datetime.fromtimestamp(end_time).strftime("%Y-%m-%d %H:%M:%S"),
                        "duration": duration
                    })
                    self.switch_counter += 1  # Increment switch counter

                # Update current app
                self.current_app = active_app
                self.start_time = time.time()

                # Update GUI
                self.update_gui()

            time.sleep(1)

    def update_gui(self):
        """Updates the GUI with the latest data."""
        # Update current app
        self.current_app_label.config(text=f"Current App: {self.current_app}")

        # Update total screen time
        total_time = sum(self.total_time_per_app.values())
        self.total_time_label.config(text=f"Total Screen Time: {round(total_time / 60, 2)} mins")

        # Update treeview
        for i in self.tree.get_children():
            self.tree.delete(i)
        for app, time_spent in self.total_time_per_app.items():
            self.tree.insert("", "end", values=(app, round(time_spent / 60, 2)))

    def export_log(self):
        """Exports the usage log to a CSV file with the date in the filename."""
        # Get today's date for the filename
        today = datetime.now().strftime("%Y-%m-%d")
        file_name = f"screen_time_log_{today}.csv"

        # Combine the sessions and export them
        combined_sessions = self.combine_sessions()

        with open(file_name, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Application", "Start Time", "End Time", "Duration (seconds)", "Duration (minutes)"])

            for session in combined_sessions:
                writer.writerow([
                    session["app"],
                    session["start"],
                    session["end"],
                    round(session["duration"], 2),
                    round(session["duration"] / 60, 2)
                ])
        print(f"Log exported to {file_name}")

    def combine_sessions(self):
        """Combine overlapping or consecutive sessions into a unified log."""
        combined = []

        for app, sessions in self.usage_sessions.items():
            if not sessions:
                continue

            # Sort sessions by start time
            sessions = sorted(sessions, key=lambda x: datetime.strptime(x["start"], "%Y-%m-%d %H:%M:%S"))
            merged = [sessions[0]]

            for current in sessions[1:]:
                last = merged[-1]
                last_end = datetime.strptime(last["end"], "%Y-%m-%d %H:%M:%S")
                current_start = datetime.strptime(current["start"], "%Y-%m-%d %H:%M:%S")

                # If sessions overlap or are consecutive, merge them
                if current_start <= last_end:
                    last["end"] = max(last["end"], current["end"])
                    last["duration"] += current["duration"]
                else:
                    merged.append(current)

            # Add merged sessions for this app
            for session in merged:
                session["app"] = app
                combined.append(session)

        return combined

    def load_previous_day_data(self):
        """Load the previous day's data if available, but do not mix it with today's data."""
        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        file_name = f"screen_time_log_{yesterday}.csv"
        print(file_name)
        if os.path.exists(file_name):
            with open(file_name, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    app, start, end, duration, duration_min = row
                    # Convert to appropriate types and append to usage_sessions for viewing only
                    duration = float(duration)
                    if app not in self.usage_sessions:
                        self.usage_sessions[app] = []
                    self.usage_sessions[app].append({
                        "start": start,
                        "end": end,
                        "duration": duration
                    })
            print(f"Loaded previous day's data from {file_name}")

    def stop_tracking(self):
        """Stops the tracking loop, exports the data, and exits the application."""
        self.running = False
        self.export_log()  # Export data when the app is closed
        self.root.destroy()  # Close the application

    def view_last_day_data(self):
        """Opens a new window to view the last day's screen time data."""
        # Load the previous day's data
        self.load_previous_day_data()

        # Create a new top-level window
        preview_window = Toplevel(self.root)
        preview_window.title("Last Day's Screen Time Data")

        # Get screen width and height to center the window
        screen_width = preview_window.winfo_screenwidth()
        screen_height = preview_window.winfo_screenheight()
        window_width = 800
        window_height = 750
        # Calculate position for centering the window
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        preview_window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        preview_window.config(bg="#4a4a4a")  # Set background color for preview window

        # Add a treeview to show the data
        tree = ttk.Treeview(preview_window, columns=("App", "Total Time (mins)"), show="headings", height=10)
        tree.heading("App", text="App")
        tree.heading("Total Time (mins)", text="Total Time (mins)")
        tree.pack(fill=tk.BOTH, expand=True, pady=10)

        # Aggregate and sort apps by usage time
        sorted_apps = sorted(self.total_time_per_app.items(), key=lambda x: x[1], reverse=True)

        # Limit the CSV to show the top 10 entries
        for app, time_spent in sorted_apps[:10]:
            tree.insert("", "end", values=(
                app,
                round(time_spent / 60, 2)
            ))

        # Generate the chart
        self.create_usage_chart(sorted_apps[:10], preview_window)

        # Display switch count summary
        switch_label = ttk.Label(preview_window, text=f"Total App Switches: {self.switch_counter}", font=("Arial", 14),
                                 background="#4a4a4a", foreground="white")
        switch_label.pack(pady=10)

    def load_previous_day_data(self):
        """Load the previous day's data if available, but do not mix it with today's data."""
        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        file_name = f"screen_time_log_{yesterday}.csv"
        print(file_name)
        if os.path.exists(file_name):
            with open(file_name, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    app, start, end, duration, duration_min = row
                    # Convert to appropriate types and append to usage_sessions for viewing only
                    duration = float(duration)
                    if app not in self.total_time_per_app:
                        self.total_time_per_app[app] = 0
                    self.total_time_per_app[app] += duration

                    if app not in self.usage_sessions:
                        self.usage_sessions[app] = []
                    self.usage_sessions[app].append({
                        "start": start,
                        "end": end,
                        "duration": duration
                    })
            print(f"Loaded previous day's data from {file_name}")

    def create_usage_chart(self, sorted_apps, preview_window):
        """Generates a bar chart for the app usage with apps on the Y-axis."""
        apps = [app for app, _ in sorted_apps]
        times = [time_spent / 60 for _, time_spent in sorted_apps]  # Convert to minutes

        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(8, 6))
        fig.patch.set_facecolor('#4a4a4a')  # Set light gray background for the figure

        # Bar chart with apps on the Y-axis
        ax.barh(apps, times, color='#4a4a4a')
        ax.set_ylabel('Application')
        ax.set_xlabel('Time (Minutes)')
        ax.set_title("App Usage for Last Day", color="white")

        # Set text color to white for chart labels
        ax.tick_params(axis='both', colors='white')
        ax.yaxis.label.set_color('white')
        ax.xaxis.label.set_color('white')

        # Save the chart to a BytesIO object
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)

        # Convert image to Tkinter compatible format and display
        img = Image.open(buf)
        img = img.resize((600, 400), Image.Resampling.LANCZOS)  # Adjust the size as needed
        chart_image = ImageTk.PhotoImage(img)

        # Add the chart image to the window
        chart_label = ttk.Label(preview_window, image=chart_image)
        chart_label.image = chart_image
        chart_label.pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenTimeTrackerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.stop_tracking)  # Handle window close
    root.mainloop()
