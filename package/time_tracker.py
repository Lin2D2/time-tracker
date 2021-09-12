import json
import pyglet
import tkinter as tk

from tkinter.font import Font

from package.pages.home_page import Home as Home
from package.pages.settings_page import Settings as Settings


class TimeTracker:
    def __init__(self):
        self.config_file_path = "config.json"

        # TODO load
        self.project_menu_items = []
        self.task_menu_items = []

        try:
            with open(self.config_file_path, "r") as config_file:
                config = json.load(config_file)
                self.time_history_list = config["time_history"]
        except FileNotFoundError:
            self.time_history_list = []
            with open(self.config_file_path, "w") as config_file:
                json.dump({"time_history": []},
                          config_file)
        # UI
        self.root = tk.Tk()
        # colors
        self.primary_color = "#323232"
        secoundary = ""
        self.button_bg_color = "#414141"
        self.button_hl_color = "#505050"
        self.button_fg_color = "white"

        # root config
        self.root.title("Time Tracker")
        self.root.geometry("950x500")
        self.root.configure(background=self.primary_color)

        # TODO not working
        # pyglet.font.add_directory('resources')
        # fonts
        self.time_font = Font(family="DSEG7 Classic", size=70, weight="bold")
        self.button_font = Font(size=13)

        self.home = Home(self)
        self.settings = Settings(self)

        self.draw_home()

    def run(self):
        self.root.mainloop()

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()
            widget.grid_forget()

    def draw_home(self):
        self.home.pack(fill=tk.BOTH)
        self.home.pack_propagate(False)
        self.home.draw()

    def draw_settings(self):
        self.settings.pack(fill=tk.BOTH)
        self.settings.pack_propagate(False)
        self.settings.draw()
