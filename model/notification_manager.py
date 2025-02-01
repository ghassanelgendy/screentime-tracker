# model/notification_manager.py
from win10toast import ToastNotifier

class NotificationManager:
    def __init__(self):
        self.toaster = ToastNotifier()

    def show_break_notification(self):
        self.toaster.show_toast("Break Time!", "Take a 5-minute break!", duration=5)

    def show_motivational_message(self, message):
        self.toaster.show_toast("Motivational Message", message, duration=5)