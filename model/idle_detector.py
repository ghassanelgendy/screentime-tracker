# model/idle_detector.py
import ctypes
import time

class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.c_uint),
        ("dwTime", ctypes.c_ulong)
    ]

class IdleDetector:
    def __init__(self):
        self.last_input_info = LASTINPUTINFO()
        self.last_input_info.cbSize = ctypes.sizeof(LASTINPUTINFO)

    def get_idle_time(self):
        """Get the system idle time in seconds."""
        ctypes.windll.user32.GetLastInputInfo(ctypes.byref(self.last_input_info))
        millis = ctypes.windll.kernel32.GetTickCount() - self.last_input_info.dwTime
        return millis / 1000.0  # Convert to seconds