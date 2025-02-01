# model/scheduler.py
import threading

class Scheduler:
    def __init__(self, controller, interval_minutes=60):
        self.controller = controller
        self.interval = interval_minutes * 60  # Convert minutes to seconds
        self.timer = None

    def start(self):
        """Start the auto-export scheduler."""
        self._schedule_next()

    def _schedule_next(self):
        """Schedule the next auto-export."""
        self.controller.export_data()
        self.timer = threading.Timer(self.interval, self._schedule_next)
        self.timer.start()

    def stop(self):
        """Stop the auto-export scheduler."""
        if self.timer:
            self.timer.cancel()