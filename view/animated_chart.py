# view/animated_chart.py
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation

class AnimatedChartFrame:
    def __init__(self, parent, controller):
        self.controller = controller
        self.fig = Figure(figsize=(6, 4))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack()

        self.ani = FuncAnimation(self.fig, self.update_chart, interval=1000)

    def update_chart(self, frame):
        """Update the chart with the latest data."""
        self.ax.clear()
        data = self.controller.get_summary_data()
        apps = [d['app'] for d in data]
        durations = [d['duration'] for d in data]
        self.ax.bar(apps, durations)
        self.ax.set_title("Live App Usage")