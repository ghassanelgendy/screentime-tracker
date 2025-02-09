# view/gui.py
from tkinter import Tk, Canvas, Button, PhotoImage, Label
from pathlib import Path
import random

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Ghassan\Documents\build\assets\frame0")

# view/gui.py

class Application:
    def __init__(self):
        self.controller = None  # Initialize without a controller
        self.window = Tk()
        self.window.geometry("980x653")
        self.window.configure(bg="#293E73")
        self.assets_path = Path(__file__).parent.parent / "assets" / "frame0"
        self.canvas = Canvas(
            self.window,
            bg="#293E73",
            height=653,
            width=980,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.button_images = []
        self.images = []

        # Add labels to display data
        self.total_time_label = Label(self.window, text="Total Time: 0h 0m")
        self.total_time_label.pack()

        self.switch_count_label = Label(self.window, text="Switch Counts: None")
        self.switch_count_label.pack()

        self.total_switch_count_label = Label(self.window, text="Total Switch Counts: None")
        self.total_switch_count_label.pack()

        self.setup_canvas()
        self.create_buttons()
        self.setup_additional_buttons()

    def set_controller(self, controller):
        """Assign the controller after creation"""
        self.controller = controller
        self.controller.start_tracking()  # Start tracking after controller is assigned

        
    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)

    def setup_canvas(self):
        # Rectangles
        self.canvas.create_rectangle(0.0, 38.0, 980.0, 155.0, fill="#D0D0D0", outline="")
        self.canvas.create_rectangle(0.0, 0.0, 980.0, 35.0, fill="#D9D9D9", outline="")
        self.canvas.create_rectangle(
            60.0, 232.0, 920.0, 303.0, fill="#0F1C3C", outline=""
        )

        # Text elements
        self.canvas.create_text(
            465.0, 57.0, anchor="nw", text="G-ZONE", fill="#0F1A36", font=("Cairo Black", 40 * -1)
        )

        # Define self.main_text
        self.main_text = self.canvas.create_text(
            488.0, 267.0, anchor="center", text="Initial Text", fill="#D9D9D9", font=("Cairo Black", 32 * -1)
        )
    def _update_view_loop(self):
        while self.is_running:
            # Fetch data from the model
            sessions = self.model.data_manager.get_merged_sessions()
            switch_counts = self.model.data_manager.get_switch_counts()
            total_switches = self.model.data_manager.get_total_switch_counts()
            time_based_data = {
                'hour': self.model.data_manager.get_time_based_data('hour'),
                'day': self.model.data_manager.get_time_based_data('day'),
                'week': self.model.data_manager.get_time_based_data('week')
            }

            # Update the view with all data
            self.view.update_view(
                sessions=sessions,
                switch_counts=switch_counts,
                total_switches=total_switches,
                time_based_data=time_based_data
            )

        time.sleep(0.001)  # Update every 5 seconds/
    def update_time_based_data(self, time_based_data):
        """
        Update the GUI with time-based data (hourly, daily, weekly).
        
        Args:
            time_based_data: Dictionary containing time-based data.
        """
        # # Example: Display daily usage
        # if 'day' in time_based_data:
        #     daily_data = time_based_data['day']
        #     daily_usage = sum(session['duration'] for session in daily_data)
        #     daily_usage_str = f"{int(daily_usage // 3600)}h {int((daily_usage % 3600) // 60)}m"
        #     self.canvas.itemconfig(self.totaltime, text=daily_usage_str)

        # # Example: Display hourly usage
        # if 'hour' in time_based_data:
        #     hourly_data = time_based_data['hour']
        #     # Update hourly usage display (if you have a placeholder for it)
        pass
    def update_top_apps(self, sessions):
        """
        Update the GUI with the top apps based on session data.
        
        Args:
            sessions: List of session data (app, duration, switch_count).
        """
        # Example: Display top apps
        top_apps = sorted(sessions, key=lambda x: x['total_duration'], reverse=True)
        for i, app_data in enumerate(top_apps[:5]):
            app_name = app_data['app_name']
            duration = app_data['total_duration']
            duration_str = f"{int(duration // 60)} mins"
            # Update canvas text elements with app_name and duration_str
    def update_stats(self, stats):
        """
        Update the GUI with additional statistics.
        
        Args:
            stats: Dictionary containing statistics (e.g., total switches, idle time).
        """
        # Example: Display total idle time
        if 'total_idle' in stats:
            idle_time = stats['total_idle']
            idle_time_str = f"{int(idle_time // 3600)}h {int((idle_time % 3600) // 60)}m"
            # Update a label or canvas text element with idle_time_str
            pass

        # Example: Display total switches
        if 'total_switches' in stats:
            total_switches = stats['total_switches']
            # Update a label or canvas text element with total_switches
            pass
    def update_view(self, sessions=None, switch_counts=None, total_switches=None, time_based_data=None, stats=None, total_time_overday=None):
        """ Update the GUI with the latest data. """
        
        # Ensure sessions is a valid list
        if not isinstance(sessions, list):
            sessions = []
        # Update the label
        self.total_time_label.config(text=f"Total Time: {total_time_overday or 'ghassan te3b wallahy'}")

        # Ensure switch_counts is iterable
        if isinstance(switch_counts, list) and all(isinstance(switch, dict) for switch in switch_counts):
            switch_counts_str = ", ".join(
                f"{switch.get('from_app', 'Unknown')}: {switch.get('switch_count', 0)}" 
                for switch in switch_counts
            )
        else:
            switch_counts_str = "None"

        # Update labels
        self.switch_count_label.config(text=f"Switch Counts: {switch_counts_str}")
        self.total_switch_count_label.config(text=f"Total Switch Counts: {total_switches or 'None'}")

        # Update the canvas with top apps if sessions are provided
        if sessions:
            self.update_top_apps(sessions)

        # Update time-based data if provided
        if time_based_data:
            self.update_time_based_data(time_based_data)

        # Update stats if provided
        if stats:
            self.update_stats(stats)

    def setup_canvas(self):
        # Rectangles
        self.canvas.create_rectangle(0.0, 38.0, 980.0, 155.0, fill="#D0D0D0", outline="")
        self.canvas.create_rectangle(0.0, 0.0, 980.0, 35.0, fill="#D9D9D9", outline="")
        self.canvas.create_rectangle(
            60.0, 232.0, 920.0, 303.0, fill="#0F1C3C", outline=""
        )
        self.canvas.create_rectangle(
            507.0, 489.0, 920.0, 535.0, fill="#D9D9D9", outline=""
        )
        self.canvas.create_rectangle(
            60.0, 489.0, 507.0, 535.0, fill="#BDBDBD", outline=""
        )
        self.canvas.create_rectangle(
            506.5191955566406, 442.0, 920.0, 489.0, fill="#BDBDBD", outline=""
        )
        self.canvas.create_rectangle(
            60.0, 442.0, 506.5191955566406, 489.0, fill="#D9D9D9", outline=""
        )
        self.canvas.create_rectangle(
            506.5191955566406, 395.0, 920.0, 442.0, fill="#D9D9D9", outline=""
        )
        self.canvas.create_rectangle(
            60.0, 395.0, 506.5191955566406, 442.0, fill="#BDBDBD", outline=""
        )
        self.canvas.create_rectangle(
            506.5191955566406, 349.0, 920.0, 395.0, fill="#BDBDBD", outline=""
        )
        self.canvas.create_rectangle(
            60.0, 349.0, 506.5191955566406, 395.0, fill="#D9D9D9", outline=""
        )
        self.canvas.create_rectangle(
            506.5191955566406, 303.0, 920.0, 349.0, fill="#D9D9D9", outline=""
        )
        self.canvas.create_rectangle(
            60.0, 303.0, 506.5191955566406, 349.0, fill="#BDBDBD", outline=""
        )
        self.canvas.create_rectangle(
            787.0, 271.0, 887.0, 303.0, fill="#D9D9D9", outline=""
        )
        self.canvas.create_rectangle(
            104.0, 271.0, 184.0, 303.0, fill="#D9D9D9", outline=""
        )

        # Text elements
        self.canvas.create_text(
            465.0, 57.0, anchor="nw", text="G-ZONE", fill="#0F1A36", font=("Cairo Black", 40 * -1)
        )
        self.main_text = self.canvas.create_text(
            488.0, 267.0, anchor="center", text="as", fill="#D9D9D9", font=("Cairo Black", 32 * -1)
        )
        self.canvas.create_text(
            526.0, 490.0, anchor="nw", text="Chrome                                       10 mins",
            fill="#101D3D", font=("Cairo Black", 24 * -1)
        )
        self.canvas.create_text(
            60.0, 490.0, anchor="nw", text="Chrome                                            5 mins",
            fill="#101D3D", font=("Cairo Black", 24 * -1)
        )
        self.canvas.create_text(
            526.0, 443.0, anchor="nw", text="Chrome                                       9 mins",
            fill="#101D3D", font=("Cairo Black", 24 * -1)
        )
        self.canvas.create_text(
            60.0, 443.0, anchor="nw", text="Chrome                                            4 mins",
            fill="#101D3D", font=("Cairo Black", 24 * -1)
        )
        self.canvas.create_text(
            526.0, 396.0, anchor="nw", text="Chrome                                       8 mins",
            fill="#101D3D", font=("Cairo Black", 24 * -1)
        )
        self.canvas.create_text(
            60.0, 396.0, anchor="nw", text="Chrome                                            3 mins",
            fill="#101D3D", font=("Cairo Black", 24 * -1)
        )
        self.canvas.create_text(
            526.0, 350.0, anchor="nw", text="Chrome                                       7 mins",
            fill="#101D3D", font=("Cairo Black", 24 * -1)
        )
        self.canvas.create_text(
            60.0, 350.0, anchor="nw", text="Chrome                                            2 mins",
            fill="#101D3D", font=("Cairo Black", 24 * -1)
        )
        self.canvas.create_text(
            526.0, 304.0, anchor="nw", text="Chrome                                       6 mins",
            fill="#101D3D", font=("Cairo Black", 24 * -1)
        )
        self.canvas.create_text(
            60.0, 304.0, anchor="nw", text="Chrome                                            1  mins",
            fill="#101D3D", font=("Cairo Black", 24 * -1)
        )
        self.total_switches = self.canvas.create_text(
            815.0, 271.0, anchor="nw", text="2131", fill="#101D3D", font=("Cairo Black", 20 * -1)
        )
        self.canvas.create_text(
            789.0, 240.0, anchor="nw", text="Total Switches", fill="#D9D9D9", font=("Cairo Black", 15 * -1)
        )
        self.totaltime =self.canvas.create_text(
             144.0, 287.0, anchor="center", text="24 Hr", fill="#101D3D", font=("Cairo Black", 20 * -1)
        )
        self.canvas.create_text(
            109.0, 240.0, anchor="nw", text="Total Time", fill="#D9D9D9", font=("Cairo Black", 15 * -1)
        )

        # Images
        image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.images.append(image_image_1)
        self.canvas.create_image(426.0, 97.0, image=image_image_1)


    def create_buttons(self):
        # Modify buttons to use controller methods
        self.create_button(
            x=60.0, y=570.0,
            normal_img="yesterday_btn.png",
            hover_img="yesterday_btn_hover.png",
            command=self.controller.show_yesterday_data,
            width=189.0, height=44.0
        )
        self.create_button(
            x=286.0, y=570.0,
            normal_img="charts_btn.png",
            hover_img="charts_btn_hover.png",
            command=self.controller.show_charts,
            width=151.0, height=44.0
        )
        self.create_button(
            x=474.0, y=570.0,
            normal_img="export_btn.png",
            hover_img="export_btn_hover.png",
            command=self.controller.export_data,
            width=151.0, height=44.0
        )
        self.create_button(
            x=662.0, y=570.0,
            normal_img="vision_btn.png",
            hover_img="vision_btn_hover.png",
            command=self.controller.show_vision,
            width=107.0, height=44.0
        )
        self.create_button(
            x=876.0, y=570.0,
            normal_img="jarvis_btn.png",
            hover_img="jarvis_btn_hover.png",
            command=self.controller.show_jarvis,
            width=44.0, height=44.0
        )

    def setup_additional_buttons(self):
        # Window control buttons
        self.create_button(
            x=940.0798950195312, y=2.0,
            normal_img="close_btn.png",
            hover_img="close_btn_hover.png",
            command=self.window.quit,
            width=30.09, height=30.09
        )
        self.create_button(
            x=904.0, y=2.0,
            normal_img="minimize_btn.png",
            hover_img="minimize_btn_hover.png",
            command=self.window.iconify,
            width=30.0, height=30.15
        )


    def create_button(self, x, y, normal_img, hover_img, command, width, height):
        normal_img_path = self.relative_to_assets(normal_img)
        hover_img_path = self.relative_to_assets(hover_img)

        img_normal = PhotoImage(file=normal_img_path)
        img_hover = PhotoImage(file=hover_img_path)

        # Save references to prevent garbage collection
        self.button_images.append(img_normal)
        self.button_images.append(img_hover)

        button = Button(
            self.window,
            image=img_normal,
            borderwidth=0,
            highlightthickness=0,
            command=command,
            relief="flat",
            activebackground="#293E73"
        )
        button.place(x=x, y=y, width=width, height=height)

        # Bind hover events
        button.bind("<Enter>", lambda e: button.config(image=img_hover))
        button.bind("<Leave>", lambda e: button.config(image=img_normal))
        # Elhagat ely feltitlebar
        if(y == 2):
            button.config(activebackground="#D9D9D9")
        return button

    def create_buttons(self):
        # Main action buttons
        self.create_button(
            x=60.0, y=570.0,
            normal_img="yesterday_btn.png",
            hover_img="yesterday_btn_hover.png",
            command=lambda: print("yesterday_btn clicked"),
            width=189.0, height=44.0
        )
        self.create_button(
            x=286.0, y=570.0,
            normal_img="charts_btn.png",
            hover_img="charts_btn_hover.png",
            command=lambda: print("charts_btn clicked"),
            width=151.0, height=44.0
        )
        self.create_button(
            x=474.0, y=570.0,
            normal_img="export_btn.png",
            hover_img="export_btn_hover.png",
            command=lambda: print("export btn clicked"),
            width=151.0, height=44.0
        )
        self.create_button(
            x=662.0, y=570.0,
            normal_img="vision_btn.png",
            hover_img="vision_btn_hover.png",
            command=lambda: print("vision_btn clicked"),
            width=107.0, height=44.0
        )
        self.create_button(
            x=876.0, y=570.0,
            normal_img="jarvis_btn.png",
            hover_img="jarvis_btn_hover.png",
            command=lambda: print("jarvis_btn clicked"),
            width=44.0, height=44.0
        )

    def run(self):
        self.window.resizable(False, False)
        self.window.mainloop()