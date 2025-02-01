# controller.py
import time
import threading
from model.app_monitor import AppMonitor
from model.data_manager import DataManager

class Controller:
    def __init__(self, model):
        self.model = model
        
        # Initialize the AppMonitor
        self.app_monitor = AppMonitor(self.model.data_manager)
        
        # Flag to control the update loop
        self.is_running = False

    def start_tracking(self):
        """Start tracking app switches and updating the view."""
        self.is_running = True
        self.app_monitor.start_tracking()
        
        # Start a thread to periodically update the view
        threading.Thread(target=self._update_view_loop, daemon=True).start()

    def stop_tracking(self):
        """Stop tracking app switches."""
        self.is_running = False
        self.app_monitor.is_tracking = False
    def _update_view_loop(self):
        """Periodically fetch data and update the view."""
        while self.is_running:
            # Fetch data from the model
            sessions = self.model.data_manager.get_merged_sessions()
            switch_counts = self.model.data_manager.get_switch_counts()
            
            # Update the view
            self.view.update_view(sessions, switch_counts)
            
            # Wait for 5 seconds before updating again
            time.sleep(5)
            
            while self.is_running:
                # Fetch data from the model
                sessions = self.model.data_manager.get_merged_sessions()
                switch_counts = self.model.data_manager.get_switch_counts()
                
                # Update the view (this will be implemented in the View class)
                self._update_view(sessions, switch_counts)
                
                # Wait for a short period before updating again
                time.sleep(5)  # Update every 5 seconds

    def _update_view(self, sessions, switch_counts):
        """
        Update the view with the latest data.
        
        Args:
            sessions (list): List of session data (app, duration, switch_count).
            switch_counts (list): List of switch counts (from_app, switch_count).
        """
        # This method will be implemented in the View class
        pass

    def show_yesterday_data(self):
        """Fetch and display yesterday's data."""
        data = self.model.data_manager.get_yesterday_data()
        # Update GUI with yesterday's data

    def show_charts(self):
        """Display charts."""
        self.model.scheduler.start()

    def export_data(self):
        """Export the tracked data to a CSV file."""
        self.model.data_manager.export_csv()

    def get_motivational_message(self):
        """Get a random motivational message."""
        return self.model.motivational_messages.get_message("productive")

    def update_categories(self, categories):
        """Update app categories."""
        self.model.category_manager.update(categories)

    def set_idle_threshold(self, seconds):
        """Set the idle time threshold."""
        self.model.idle_detector.set_threshold(seconds)

    def schedule_auto_export(self, interval_minutes):
        """Schedule auto-export at regular intervals."""
        self.model.scheduler.start(interval_minutes)

    def show_vision(self):
        """Display the vision or motivational message."""
        self.model.vision.show()

    def show_jarvis(self):
        """Display Jarvis-related content."""
        self.model.jarvis.show()