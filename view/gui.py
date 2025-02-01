# view/gui.py
from tkinter import Tk, Canvas, Button, PhotoImage, Label
from pathlib import Path
import random

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Ghassan\Documents\build\assets\frame0")

# view/gui.py
class Application:
    def __init__(self, controller):
        self.controller = controller
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
            highlightthickness = 0,
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

        self.setup_canvas()
        self.create_buttons()
        self.setup_additional_buttons()
        # Start tracking
        self.controller.start_tracking()

        # Bind motivational messages to a timer
        self.update_motivational_message()

        
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
    def update_view(self, sessions, switch_counts):
        """Update the GUI with the latest data."""
        # Calculate total time
        total_time = sum(session['duration'] for session in sessions)
        total_time_str = f"{int(total_time // 3600)}h {int((total_time % 3600) // 60)}m"
        
        # Format switch counts
        switch_counts_str = ", ".join(
            f"{switch['from_app']}: {switch['switch_count']}" 
            for switch in switch_counts
        )
        
        # Update the labels
        self.total_time_label.config(text=f"Total Time: {total_time_str}")
        self.switch_count_label.config(text=f"Switch Counts: {switch_counts_str}")

    def update_motivational_message(self):
        """Update the motivational message every 5 minutes."""
        message = self.controller.get_motivational_message()
        self.canvas.itemconfig(self.main_text, text=message)
        self.window.after(300000, self.update_motivational_message)  # 5 minutes
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