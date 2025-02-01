# model/__init__.py
from .app_monitor import AppMonitor
from .data_manager import DataManager
from .idle_detector import IdleDetector
from .notification_manager import NotificationManager
from .category_manager import CategoryManager
from .scheduler import Scheduler
from .motivational_messages import MotivationalMessageSystem

class Model:
    def __init__(self):
        self.data_manager = DataManager()
        self.app_monitor = AppMonitor(self.data_manager)
        self.idle_detector = IdleDetector()
        self.notifier = NotificationManager()
        self.category_manager = CategoryManager()
        self.scheduler = Scheduler(self)
        self.motivational_messages = MotivationalMessageSystem()