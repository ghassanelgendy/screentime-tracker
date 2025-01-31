import time
import win32gui
import win32process
import psutil
import threading
import pandas as pd
import ctypes
from datetime import datetime

class App:
    def __init__(self, name):
        self.name = name
        self.total_time = 0  # in seconds
        self.usage_sessions = []

    def add_session(self, start_time, end_time):
        """Add a session of usage for this app."""
        duration = end_time - start_time
        if duration < 2:  # Ignore very short sessions
            return

        if self.usage_sessions and self.usage_sessions[-1]['end'] == start_time:
            # Combine this session with the previous one
            self.usage_sessions[-1]['end'] = datetime.fromtimestamp(end_time).strftime("%Y-%m-%d %H:%M:%S")
            self.usage_sessions[-1]['duration'] += duration
        else:
            self.usage_sessions.append({
                "start": datetime.fromtimestamp(start_time).strftime("%Y-%m-%d %H:%M:%S"),
                "end": datetime.fromtimestamp(end_time).strftime("%Y-%m-%d %H:%M:%S"),
                "duration": duration
            })
        self.total_time += duration

    def get_formatted_total_time(self):
        """Get the formatted total time."""
        return self.format_duration(self.total_time)

    @staticmethod
    def format_duration(seconds):
        """Converts duration in seconds to a human-readable format."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        
        if hours > 0:
            return f"{hours} hr {minutes} min {seconds} sec"
        elif minutes > 0:
            return f"{minutes} min {seconds} sec"
        else:
            return f"{seconds} sec"

class ScreenTimeTracker:
    IDLE_THRESHOLD = 3  # 2 minutes (120 seconds)

    def __init__(self):
        self.current_app = None
        self.start_time = time.time()
        self.apps = {}  # Dictionary to store App objects by name
        self.total_screen_time = 0
        self.app_switch_count = 0
        self.running = True
        self.idle_start_time = None
        self.track_thread = threading.Thread(target=self.track_screen_time, daemon=True)
        self.track_thread.start()
        self.export_thread = threading.Thread(target=self.auto_export_log, daemon=True)
        self.export_thread.start()

    def get_active_window_exe(self):
        """Fetch the executable name of the currently active window."""
        try:
            hwnd = win32gui.GetForegroundWindow()
            if hwnd == 0:
                return "Unknown"
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)
            exe_name = process.name().replace('.exe', '')

            if exe_name == "msedge":
                return self.get_edge_tab_title(hwnd)
            return exe_name
        except Exception:
            return "Unknown Tab Name"

    def get_edge_tab_title(self, hwnd):
        """Extracts the active tab title for Microsoft Edge."""
        title = win32gui.GetWindowText(hwnd)
        if " - Microsoft Edge" in title:
            title = title.replace(" - Microsoft Edge", "")
        if " and " in title:
            title = title.split(" and ")[0]
        if " - " in title:
            title = title.split(" - ")[0]
        return f"Edge: {title}"

    def get_idle_time(self):
        """Returns the idle time in seconds."""
        class LASTINPUTINFO(ctypes.Structure):
            _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_ulong)]

        lii = LASTINPUTINFO()
        lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
        if ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii)):
            elapsed = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
            return elapsed / 1000.0  
        return 0

    def merge_consecutive_entries(self, data):
        """Merge consecutive entries of the same application."""
        if not data:
            return []
        merged_data = [data[0]]
        for entry in data[1:]:
            last_entry = merged_data[-1]
            if entry[0] == last_entry[0]:  # Same application
                last_entry[2] = entry[2]  # Update end time
                last_entry[3] += entry[3]  # Sum duration
            else:
                merged_data.append(entry)
        return merged_data

    def categorize_app(self, app_name):
        """Categorize application into predefined categories."""
        categories = {
            'social media': ['Facebook', 'Instagram', 'Twitter', 'TikTok'],
            'coding': ['py', 'VSCode', 'PyCharm', 'Eclipse'],
            'creative': ['Photoshop', 'Illustrator', 'Premiere'],
            'browser': ['Chrome', 'Firefox', 'Edge'],
            'other': []
        }
        for category, apps in categories.items():
            if any(app in app_name for app in apps):
                return category
        return 'other'

    def track_screen_time(self):
        """Tracks screen time for each application in the background."""
        while self.running:
            idle_time = self.get_idle_time()
            if idle_time >= self.IDLE_THRESHOLD:
                if self.current_app != "Idle Time":
                    end_time = time.time()
                    if self.current_app:
                        app = self.apps.get(self.current_app)
                        if app:
                            app.add_session(self.start_time, end_time)
                            self.total_screen_time += (end_time - self.start_time)
                        if self.current_app != "Idle Time":
                            self.app_switch_count += 1
                    
                    self.current_app = "Idle Time"
                    self.start_time = time.time()
                    if "Idle Time" not in self.apps:
                        self.apps["Idle Time"] = App("Idle Time")
                    
                    print("\n🟡 System is idle... Logging idle time.")
                
                time.sleep(1)
                continue  

            active_app = self.get_active_window_exe()
            
            if active_app != self.current_app:
                if self.current_app:
                    end_time = time.time()
                    app = self.apps.get(self.current_app)
                    if app:
                        app.add_session(self.start_time, end_time)
                        self.total_screen_time += (end_time - self.start_time)
                    self.app_switch_count += 1
                    if self.current_app == "Idle Time":
                        self.app_switch_count -= 2
                    print(f"\nCurrent App: {self.current_app} - {App.format_duration(end_time - self.start_time)}")
                    print(f"Total Screen Time: {App.format_duration(self.total_screen_time)}")
                    print(f"App Switch Count: {self.app_switch_count}")
                    print("=================")

                self.current_app = active_app
                if active_app not in self.apps:
                    self.apps[active_app] = App(active_app)
                self.start_time = time.time()

            time.sleep(1)

    def export_log(self):
        """Exports the usage log to a CSV file using pandas."""
        today = datetime.now().strftime("%Y-%m-%d")
        file_name = f"screen_time_log_{today}.csv"
        
        data = []
        for app in self.apps.values():
            for session in app.usage_sessions:
                data.append([ 
                    app.name,
                    session["start"],
                    session["end"],
                    round(session["duration"], 2),
                    self.categorize_app(app.name)
                ])
        
        merged_data = self.merge_consecutive_entries(data)
        df = pd.DataFrame(merged_data, columns=["Application", "Start Time", "End Time", "Duration (seconds)", "App Type"])
        df.to_csv(file_name, index=False, encoding="utf-8")
        
        print(f"📁 Log exported to {file_name}")

    def auto_export_log(self):
        """Automatically exports the log every 5 seconds."""
        while self.running:
            time.sleep(5)
            self.export_log()

    def stop_tracking(self):
        """Stops tracking and exports the log."""
        self.running = False
        if self.current_app:
            self.apps[self.current_app].add_session(self.start_time, time.time())
        self.export_log()

if __name__ == "__main__":
    tracker = ScreenTimeTracker()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping tracker...")
        tracker.stop_tracking()
