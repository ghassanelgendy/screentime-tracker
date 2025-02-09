# model/idle_detector.py
import ctypes

class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_ulong)]

class IdleDetector:
    def __init__(self):
        self.last_input_info = LASTINPUTINFO()
        self.last_input_info.cbSize = ctypes.sizeof(LASTINPUTINFO)
        self.threshold = 30000  # Default: 5 minutes

    def get_idle_sec(self):
        if ctypes.windll.user32.GetLastInputInfo(ctypes.byref(self.last_input_info)):
            millis = ctypes.windll.kernel32.GetTickCount() - self.last_input_info.dwTime
            return millis // 1000
        return 0  # Return 0 if function fails

    def set_threshold(self, seconds):
        self.threshold = seconds
