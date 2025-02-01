# model/app_monitor.py
import time
import threading
import psutil
import win32gui
import win32process

class AppMonitor:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.is_tracking = False
        self.last_app = None
        self.last_switch_time = time.time()

    def get_active_app(self):
        hwnd = win32gui.GetForegroundWindow()
        pid = win32process.GetWindowThreadProcessId(hwnd)[1]
        try:
            return psutil.Process(pid).name().split('.exe')[0]
        except:
            return "System"

    def start_tracking(self):
        self.is_tracking = True
        threading.Thread(target=self._track_loop, daemon=True).start()

    def _track_loop(self):
        while self.is_tracking:
            current_app = self.get_active_app()
            if current_app != self.last_app:
                self.data_manager.log_app_switch(
                    self.last_app, 
                    current_app, 
                    time.time()
                )
                self.last_app = current_app
            time.sleep(1)