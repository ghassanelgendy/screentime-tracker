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
        duration = end_time - start_time
        if duration < 2:
            return

        if self.usage_sessions and self.usage_sessions[-1]['end'] == start_time:
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
        return self.format_duration(self.total_time)

    @staticmethod
    def format_duration(seconds):
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        return f"{hours} hr {minutes} min {seconds} sec" if hours else (f"{minutes} min {seconds} sec" if minutes else f"{seconds} sec")

class ScreenTimeTracker:
    IDLE_THRESHOLD = 120  # 2 minutes

    def __init__(self):
        self.current_app = None
        self.start_time = time.time()
        self.apps = {}
        self.total_screen_time = 0
        self.app_switch_count = 0
        self.running = True
        self.lock = threading.Lock()
        
        self.track_thread = threading.Thread(target=self.track_screen_time, daemon=True)
        self.track_thread.start()
        self.export_thread = threading.Thread(target=self.auto_export_log, daemon=True)
        self.export_thread.start()

    def get_active_window_exe(self):
        try:
            hwnd = win32gui.GetForegroundWindow()
            if hwnd == 0:
                return "Unknown"
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)
            exe_name = process.name().replace('.exe', '')
            title = win32gui.GetWindowText(hwnd)
            return f"Edge: {title.split(' - ')[0]}" if exe_name == "msedge" and title else exe_name
        except Exception:
            return "Unknown"

    def get_idle_time(self):
        class LASTINPUTINFO(ctypes.Structure):
            _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_ulong)]
        
        lii = LASTINPUTINFO()
        lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
        if ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii)):
            return (ctypes.windll.kernel32.GetTickCount() - lii.dwTime) / 1000.0
        return 0

    def track_screen_time(self):
        while self.running:
            idle_time = self.get_idle_time()
            active_app = "Idle Time" if idle_time >= self.IDLE_THRESHOLD else self.get_active_window_exe()
            
            with self.lock:
                if active_app != self.current_app:
                    end_time = time.time()
                    if self.current_app and self.current_app in self.apps:
                        self.apps[self.current_app].add_session(self.start_time, end_time)
                        self.total_screen_time += (end_time - self.start_time)
                        self.app_switch_count += 1 if self.current_app != "Idle Time" else -2

                    self.current_app = active_app
                    if active_app not in self.apps:
                        self.apps[active_app] = App(active_app)
                    self.start_time = time.time()
            
            time.sleep(1)

    def export_log(self):
        today = datetime.now().strftime("%Y-%m-%d")
        file_name = f"screen_time_log_{today}.csv"
        
        with self.lock:
            data = [[app.name, session["start"], session["end"], round(session["duration"], 2)]
                    for app in self.apps.values() for session in app.usage_sessions]
            df = pd.DataFrame(data, columns=["Application", "Start Time", "End Time", "Duration (seconds)"])
            df.to_csv(file_name, index=False, encoding="utf-8")
        
        print(f"📁 Log exported to {file_name}")

    def auto_export_log(self):
        while self.running:
            time.sleep(30)
            self.export_log()

    def stop_tracking(self):
        self.running = False
        with self.lock:
            if self.current_app and self.current_app in self.apps:
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
