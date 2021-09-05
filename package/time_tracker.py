import datetime
import tkinter as tk


class TimeTracker:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.total_time = None
        self.current_activity = None
        self.paused = False
        self.started = False

        # UI
        self.master = tk.Tk()

    def run(self):
        self.master.mainloop()

