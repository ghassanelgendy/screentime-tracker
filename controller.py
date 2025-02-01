# controller.py
class Controller:
    def __init__(self, model):
        self.model = model

    def show_yesterday_data(self):
        data = self.model.data_manager.get_yesterday_data()
        # Update GUI with yesterday's data

    def show_charts(self):
        self.model.scheduler.start()

    def export_data(self):
        self.model.data_manager.export_csv()

    def get_motivational_message(self):
        return self.model.motivational_messages.get_message("productive")

    def update_categories(self, categories):
        self.model.category_manager.update(categories)

    def set_idle_threshold(self, seconds):
        self.model.idle_detector.set_threshold(seconds)

    def schedule_auto_export(self, interval_minutes):
        self.model.scheduler.start(interval_minutes)
        
    def show_vision(self):
        self.model.vision.show()

    def show_jarvis(self):
        self.model.jarvis.show()