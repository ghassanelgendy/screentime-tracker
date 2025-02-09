# controller.py

import threading
import time
from datetime import datetime, timedelta
from model.app_monitor import AppMonitor
from model.data_manager import DataManager

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.app_monitor = AppMonitor(self.model.data_manager)
        self.is_running = False
        self.update_interval = 5  # seconds
        self.last_daily_update = datetime.now().date()

    def start_tracking(self):
        """Start tracking app usage and initialize update loop"""
        if not self.is_running:
            self.is_running = True
            self.app_monitor.start_tracking()
            self._schedule_view_update()
            self._schedule_daily_updates()

    def stop_tracking(self):
        """Stop all tracking activities"""
        self.is_running = False
        self.app_monitor.stop_tracking()

    def _schedule_view_update(self):
        """Schedule periodic view updates using threading"""
        def update_loop():
            while self.is_running:
                start_time = time.time()
                self._update_view_data()
                elapsed = time.time() - start_time
                sleep_time = max(0, self.update_interval - elapsed)
                time.sleep(sleep_time)

        threading.Thread(target=update_loop, daemon=True).start()

    def _schedule_daily_updates(self):
        """Handle daily maintenance tasks"""
        def daily_update():
            while self.is_running:
                now = datetime.now()
                if now.date() != self.last_daily_update:
                    self.model.data_manager.update_daily_stats()
                    self.last_daily_update = now.date()
                time.sleep(3600)  # Check every hour

        threading.Thread(target=daily_update, daemon=True).start()

    def _update_view_data(self):
        """Collect data and update the view"""
        try:
            # Get fresh data from model
            timeframes = ['hour', 'day', 'week']
            time_based_data = {
                timeframe: self.model.data_manager.get_time_based_data(timeframe)
                for timeframe in timeframes
            }

            stats = {
                'total_switches': self.model.data_manager.get_app_switch_count(),
                'total_idle': self.model.data_manager.get_total_idle_time('day'),
                'daily_usage': time_based_data['day'],  # Avoid duplicate calls
                'top_apps': self.model.data_manager.get_merged_sessions('day')
            }
            print(stats['total_switches'], "total_switches====================")  # Debug print
            # Retrieve switch count data if needed
            switch_counts = self.model.data_manager.get_total_app_switch_count()
            print("DEBUG: top_apps data ->", stats['top_apps'])
            # Safely extract total_duration with a default value of 0
            total_time_seconds = self.model.data_manager.get_total_usage_today()
            print(total_time_seconds, "total_time in seconds for all apps=============")  # Debug print
            # Update view with new data
            self.view.update_view(
                sessions=stats['top_apps'],
                switch_counts=switch_counts,  # Corrected to retrieve real switch count
                total_switches=stats['total_switches'],
                time_based_data=time_based_data,
                stats=stats,
                total_time_overday=total_time_seconds
            )

        except Exception as e:
            print(f"Error updating view: {str(e)}")

    def show_timeframe_data(self, timeframe):
        """Handle timeframe-specific data requests"""
        data = self.model.data_manager.get_time_based_data(timeframe)
        self.view.display_timeframe_data(timeframe, data)

    def export_data(self, timeframe='all'):
        """Export data with time filtering support"""
        filename = f"screentime_export_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
        
        if timeframe == 'all':
            data = self.model.data_manager.get_time_based_data('all')
        else:
            data = self.model.data_manager.get_time_based_data(timeframe)
            
        self.model.data_manager.export_to_csv(data, filename)
        return filename

    def update_categories(self, categories):
        """Update categories with validation"""
        validated = self.model.category_manager.validate_categories(categories)
        self.model.data_manager.update_categories(validated)
        self._update_view_data()

    def set_idle_threshold(self, seconds):
        """Update idle detection threshold"""
        self.model.idle_detector.set_threshold(seconds)
        self.app_monitor.update_idle_threshold(seconds)

    def get_motivational_message(self):
        """Get context-aware motivational message"""
        usage_data = self.model.data_manager.get_time_based_data('day')
        return self.model.motivational_messages.get_message_based_on_usage(usage_data)

    def schedule_auto_export(self, interval_hours):
        """Schedule automatic exports"""
        def auto_export_task():
            while self.is_running:
                self.export_data()
                time.sleep(interval_hours * 3600)
                
        threading.Thread(target=auto_export_task, daemon=True).start()

    def shutdown(self):
        """Clean shutdown procedure"""
        self.stop_tracking()
        self.model.data_manager.update_daily_stats()
        self.model.data_manager.close_connections()
