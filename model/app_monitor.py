# model/app_monitor.py
import time
import threading
import psutil
import win32gui
import win32process
import win32api
from datetime import datetime, timedelta

class AppMonitor:
    def __init__(self, data_manager, idle_threshold=10):
        self.data_manager = data_manager
        self.is_tracking = False
        self.current_app_id = None
        self.last_input_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        self.idle_threshold = idle_threshold  # seconds
        self.idle_start = None
        self.lock = threading.Lock()

    def get_active_app_info(self):
        """Get current foreground app with executable path"""
        try:
            hwnd = win32gui.GetForegroundWindow()
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)
            return {
                'name': process.name(),
                'exe': process.exe(),
                'pid': pid
            }
        except (psutil.NoSuchProcess, win32process.error, win32gui.error):
            return {'name': 'System', 'exe': '', 'pid': 404}

    def get_last_input_time(self):
        """Get system's last input time in seconds"""
        last_input = win32api.GetLastInputInfo()
        tick_diff = win32api.GetTickCount() - last_input
        return tick_diff / 1000.0

    def is_system_idle(self):
        """Check if system has been idle longer than threshold"""
        return self.get_last_input_time() > self.idle_threshold

    def start_tracking(self, interval=1):
        """Start monitoring with specified check interval"""
        self.is_tracking = True
        # Start app tracking thread
        threading.Thread(target=self._app_tracking_loop, 
                        args=(interval,), daemon=True).start()
        # Start idle detection thread
        threading.Thread(target=self._idle_detection_loop, 
                        args=(interval,), daemon=True).start()

    def stop_tracking(self):
        """Stop all tracking activities"""
        with self.lock:
            self.is_tracking = False
            # Finalize any ongoing idle session
            if self.idle_start:
                self._log_idle_session()

    def _app_tracking_loop(self, interval):
        """Main loop for tracking application usage"""
        while self.is_tracking: 
            try:
                # Skip tracking if system is idle
                if not self.is_system_idle():
                    app_info = self.get_active_app_info()
                    app_id = self.data_manager.get_or_create_app(
                        app_info['name'], 
                        app_info['exe']
                    )
                    
                    with self.lock:
                        if app_id != self.current_app_id:
                            self._handle_app_switch(app_id)
                            
                time.sleep(interval)
                
            except Exception as e:
                print(f"Tracking error: {str(e)}")
                time.sleep(5)
    def _idle_detection_loop(self, interval):
        """Monitor for idle periods"""
        while self.is_tracking:
            try:
                is_idle = self.is_system_idle()  # Call once per loop iteration
                
                with self.lock:
                    if is_idle and not self.idle_start:
                        # System just went idle
                        self.idle_start = datetime.now()
                        self.current_app_id = None  # Only reset if necessary

                    elif not is_idle and self.idle_start:
                        # System is active again; log idle session and reset
                        self._log_idle_session()
                        self.idle_start = None  # Reset after logging
                
                time.sleep(interval)

            except Exception as e:
                print(f"Idle detection error: {str(e)}")
                time.sleep(5)  # Prevent excessive error looping

    def _handle_app_switch(self, new_app_id):
        """Handle application switch logic"""
        from_app_id = self.current_app_id
        self.current_app_id = new_app_id
        
        # Log the switch
        if from_app_id is not None:
            self.data_manager.log_app_switch(
                from_app_id, 
                new_app_id
            )
        else:
            # Initial app registration
            self.data_manager.log_app_switch(None, new_app_id)

    def _log_idle_session(self):
        """Record completed idle period"""
        if self.idle_start:
            end_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            self.data_manager.log_idle_time(self.idle_start, end_time)
            self.idle_start = None

    def update_idle_threshold(self, new_threshold):
        """Update the idle detection threshold"""
        with self.lock:
            self.idle_threshold = new_threshold

    def get_current_app_id(self):
        """Get currently tracked application ID"""
        with self.lock:
            return self.current_app_id