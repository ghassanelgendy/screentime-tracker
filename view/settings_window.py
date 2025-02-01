# view/settings_window.py
from tkinter import Toplevel, Label, Entry, Button, Frame

class SettingsWindow(Toplevel):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Settings")
        self.geometry("400x300")
        self._setup_ui()

    def _setup_ui(self):
        Label(self, text="App Categories").pack()

        self.category_entries = {}
        for app, category in self.controller.get_categories().items():
            frame = Frame(self)
            Label(frame, text=app).pack(side="left")
            entry = Entry(frame)
            entry.insert(0, category)
            entry.pack(side="left")
            self.category_entries[app] = entry
            frame.pack()

        Button(self, text="Save", command=self.save).pack()

    def save(self):
        categories = {app: entry.get() for app, entry in self.category_entries.items()}
        self.controller.update_categories(categories)