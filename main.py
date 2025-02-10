import time
import sqlite3
import pygetwindow as gw
import threading
import signal
import sys
from datetime import datetime

# Connect to SQLite database
conn = sqlite3.connect("screen_time.db", check_same_thread=False)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS screen_time (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    window_name TEXT,
    duration INTEGER,
    switch_count INTEGER,
    hour INTEGER,
    day INTEGER,
    month INTEGER,
    year INTEGER
)
""")
conn.commit()

# Dictionary to store start time and switch count
window_start_time = {}
switch_count = {}
last_window = None  # Track the last active window
last_switch_time = None

# Function to get the active window title
def get_active_window():
    try:
        active_window = gw.getActiveWindow()
        if active_window:
            title = active_window.title
            if title and "Task Switching" not in title:  # Ignore "Task Switching" window
                return title
    except:
        return None
    return None

# Function to update the database
def update_database(window_name, duration, switches):
    now = datetime.now()
    hour, day, month, year = now.hour, now.day, now.month, now.year
    
    cursor.execute("SELECT duration, switch_count FROM screen_time WHERE window_name = ? AND hour = ? AND day = ? AND month = ? AND year = ?", 
                   (window_name, hour, day, month, year))
    result = cursor.fetchone()
    print("THIS APP'S DURATION BEFORE UPDATING",result)
    if result:
        new_duration = result[0] + duration
        new_switch_count = result[1] + switches
        cursor.execute("UPDATE screen_time SET duration = ?, switch_count = ? WHERE window_name = ? AND hour = ? AND day = ? AND month = ? AND year = ?", 
                       (new_duration, new_switch_count, window_name, hour, day, month, year))
    else:
        cursor.execute("INSERT INTO screen_time (window_name, duration, switch_count, hour, day, month, year) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                       (window_name, duration, switches, hour, day, month, year))
    conn.commit()

# Function to get overall duration for a specific day
def get_overall_duration(day, month, year):
    cursor.execute("SELECT SUM(duration) FROM screen_time WHERE day = ? AND month = ? AND year = ?", (day, month, year))
    result = cursor.fetchone()
    return result[0] if result[0] else 0

# Background tracking function
def track_screen_time():
    global last_window, last_switch_time
    
    while True:
        current_window = get_active_window()
        now = time.time()
        
        if current_window and current_window != last_window:
            if last_window is not None:
                elapsed_time = now - last_switch_time if last_switch_time else 1
                print(get_overall_duration(9,2,2025))
                print(f"Switched to: {current_window}")
                switch_count[last_window] = switch_count.get(last_window, 0) + 1
                update_database(last_window, int(elapsed_time), 1)
            
            window_start_time[current_window] = now
            last_window = current_window
            last_switch_time = now
        
        if current_window:
            elapsed_time = now - window_start_time.get(current_window, now)
            update_database(current_window, int(elapsed_time), 0)
            window_start_time[current_window] = now
        
        time.sleep(1)  # Check every second

# Signal handler to ensure graceful shutdown
def signal_handler(sig, frame):
    print("\nStopping screen time tracker...")
    conn.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Run as daemon
if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')  # Fix UnicodeEncodeError
    tracking_thread = threading.Thread(target=track_screen_time, daemon=True)
    tracking_thread.start()
    print("Screen time tracking started. Running in the background. Press Ctrl+C to stop.")
    while True:
        time.sleep(1)  # Keep the main thread alive indefinitely
