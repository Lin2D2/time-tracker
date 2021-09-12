import time
import datetime
import os
import json
import pyglet
import tkinter as tk

from tkinter.font import Font


class TimeTracker:
    def __init__(self):
        self.config_file_path = "config.json"
        self.start_datetime = None
        self.resync_datetime = None
        self.last_time_step = None
        self.total_time = 0
        self.current_activity = None
        self.paused = False
        self.started = False

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
        primary_color = "#323232"
        secoundary = ""
        button_bg_color = "#414141"
        button_hl_color = "#505050"
        button_fg_color = "white"

        # root config
        self.root.title("Time Tracker")
        self.root.geometry("950x500")
        self.root.configure(background=primary_color)

        # TODO not working
        # pyglet.font.add_directory('resources')
        # fonts
        time_font = Font(family="DSEG7 Classic", size=70, weight="bold")
        button_font = Font(size=13)

        # definition
        time_frame = tk.Frame(self.root,
                              bg=primary_color,
                              highlightthickness=1,
                              highlightbackground=primary_color)

        self.time_text = tk.Label(time_frame,
                                  text="00:00:00",
                                  highlightthickness=1,
                                  bg=primary_color,
                                  highlightbackground=primary_color,
                                  foreground="white",
                                  height=1, width=14,
                                  font=time_font)

        # self.current_activity_input = tk.Entry(self.root,
        #                                        bg=primary_color,
        #                                        highlightthickness=1,
        #                                        highlightbackground=button_hl_color,
        #                                        font=("", 15),
        #                                        width=73)
        activity_input_frame = tk.Frame(self.root,
                                        bg=primary_color,
                                        highlightthickness=1,
                                        highlightbackground=primary_color)
        activity_input_project_menu_frame = tk.Frame(activity_input_frame,
                                                     bg=primary_color,
                                                     highlightthickness=1,
                                                     highlightbackground=primary_color)
        self.activity_input_project_menu_label = tk.Label(activity_input_project_menu_frame,
                                                          text="Project:",
                                                          highlightthickness=1,
                                                          bg=primary_color,
                                                          highlightbackground=primary_color,
                                                          foreground="white",
                                                          font=button_font)
        self.project_menu_var = tk.Variable(self.root)
        if len(self.project_menu_items) < 1:
            self.project_menu_var.set("Unset")
        else:
            self.project_menu_var.set(self.project_menu_items[0])
        self.project_menu_var.trace("w", self.project_menu_change)
        self.activity_input_project_menu = tk.OptionMenu(activity_input_project_menu_frame,
                                                         self.project_menu_var,
                                                         self.project_menu_items)
        self.activity_input_project_menu.config(highlightthickness=1,
                                                bg=primary_color,
                                                highlightbackground=primary_color,
                                                foreground="white",
                                                font=button_font,
                                                width=30,
                                                anchor='w')
        activity_input_task_menu_frame = tk.Frame(activity_input_frame,
                                                  bg=primary_color,
                                                  highlightthickness=1,
                                                  highlightbackground=primary_color)
        self.activity_input_task_menu_label = tk.Label(activity_input_task_menu_frame,
                                                       text="Task:",
                                                       highlightthickness=1,
                                                       bg=primary_color,
                                                       highlightbackground=primary_color,
                                                       foreground="white",
                                                       font=button_font)
        self.task_menu_var = tk.Variable(self.root)
        if len(self.task_menu_items) < 1:
            self.task_menu_var.set("Unset")
        else:
            self.task_menu_var.set(self.task_menu_items[0])
        self.task_menu_var.trace("w", self.task_menu_change)
        self.activity_input_task_menu = tk.OptionMenu(activity_input_task_menu_frame,
                                                      self.task_menu_var,
                                                      self.task_menu_items)
        self.activity_input_task_menu.config(highlightthickness=1,
                                             bg=primary_color,
                                             highlightbackground=primary_color,
                                             foreground="white",
                                             font=button_font,
                                             width=30,
                                             anchor='w')

        upper_button_frame = tk.Frame(self.root,
                                      background=primary_color,
                                      highlightbackground=button_hl_color,
                                      highlightthickness=1)
        self.left_button = tk.Button(upper_button_frame,
                                     bg=button_bg_color, foreground=button_fg_color,
                                     highlightthickness=1,
                                     highlightbackground=button_hl_color,
                                     text="Start", font=button_font,
                                     padx=350, pady=5,
                                     command=self.start_action_resume_action)
        self.right_button = tk.Button(upper_button_frame,
                                      bg=button_bg_color, foreground=button_fg_color,
                                      highlightthickness=1,
                                      highlightbackground=button_hl_color,
                                      text="Stopped", font=button_font,
                                      padx=350, pady=5,
                                      command=self.stop_action_save_action)
        self.right_button["state"] = tk.DISABLED

        self.list_frame = tk.Frame(self.root,
                                   background=primary_color,
                                   highlightbackground=button_hl_color,
                                   highlightthickness=1,
                                   height=230, width=880)

        list_button_frame_frame = tk.Frame(self.root,
                                           background=primary_color,
                                           highlightbackground=button_hl_color,
                                           highlightthickness=1,
                                           )
        list_button_frame = tk.Frame(list_button_frame_frame,
                                     background=primary_color,
                                     highlightbackground=button_hl_color,
                                     highlightthickness=1,
                                     )
        self.list_delete_button = tk.Button(list_button_frame,
                                            bg=button_bg_color, foreground=button_fg_color,
                                            highlightthickness=1,
                                            highlightbackground=button_hl_color,
                                            text="Delete", font=button_font,
                                            padx=130, pady=5)
        self.list_delete_button["state"] = tk.DISABLED
        self.list_edit_button = tk.Button(list_button_frame, foreground=button_fg_color,
                                          bg=button_bg_color,
                                          highlightthickness=1,
                                          highlightbackground=button_hl_color,
                                          text="Edit", font=button_font,
                                          padx=130, pady=5)
        self.list_edit_button["state"] = tk.DISABLED

        lower_button_row_frame = tk.Frame(self.root,
                                          background=primary_color,
                                          highlightbackground=button_hl_color,
                                          highlightthickness=1,
                                          )
        self.settings_button = tk.Button(lower_button_row_frame, foreground=button_fg_color,
                                         bg=button_bg_color,
                                         highlightthickness=1,
                                         highlightbackground=button_hl_color,
                                         text="Settings", font=button_font,
                                         padx=150, pady=5)
        self.about_button = tk.Button(lower_button_row_frame, foreground=button_fg_color,
                                      bg=button_bg_color,
                                      highlightthickness=1,
                                      highlightbackground=button_hl_color,
                                      text="About", font=button_font,
                                      padx=150, pady=5)
        self.help_button = tk.Button(lower_button_row_frame,
                                     bg=button_bg_color, foreground=button_fg_color,
                                     highlightthickness=1,
                                     highlightbackground=button_hl_color,
                                     text="Help", font=button_font,
                                     padx=150, pady=5)
        self.quit_button = tk.Button(lower_button_row_frame,
                                     bg=button_bg_color, foreground=button_fg_color,
                                     highlightthickness=1,
                                     highlightbackground=button_hl_color,
                                     text="Quit", font=button_font,
                                     padx=150, pady=5,
                                     command=self.quit_action)

        # layout
        time_frame.pack(fill=tk.X)
        self.time_text.pack()

        # self.current_activity_input.pack(fill=tk.X)
        activity_input_frame.pack(fill=tk.X)
        activity_input_frame.columnconfigure(0, weight=1)
        activity_input_frame.columnconfigure(1, weight=1)
        activity_input_project_menu_frame.grid(row=0, column=0)
        self.activity_input_project_menu_label.grid(row=0, column=0)
        self.activity_input_project_menu.grid(row=0, column=1)
        activity_input_task_menu_frame.grid(row=0, column=1)
        self.activity_input_task_menu_label.grid(row=0, column=0)
        self.activity_input_task_menu.grid(row=0, column=1)

        upper_button_frame.pack(fill=tk.X)
        self.left_button.grid(row=0, column=0)
        self.right_button.grid(row=0, column=1)
        upper_button_frame.columnconfigure(0, weight=1)
        upper_button_frame.columnconfigure(1, weight=1)

        self.list_frame.pack(fill=tk.BOTH)
        self.list_frame.grid_propagate(False)
        for index, time_history in enumerate(self.time_history_list):
            self.add_history_time_element(index,
                                          time_history["start_time"],
                                          time_history["end_time"],
                                          time_history["total_time"])

        list_button_frame_frame.pack(fill=tk.X)
        list_button_frame_frame.columnconfigure(0, weight=1)
        list_button_frame_frame.columnconfigure(1, weight=0)
        list_button_frame.grid(row=0, column=1)
        list_button_frame.columnconfigure(0, weight=1)
        list_button_frame.columnconfigure(1, weight=1)
        self.list_delete_button.grid(row=0, column=0)
        self.list_edit_button.grid(row=0, column=1)

        lower_button_row_frame.pack(fill=tk.X)
        self.settings_button.grid(row=0, column=0)
        self.about_button.grid(row=0, column=1)
        self.help_button.grid(row=0, column=2)
        self.quit_button.grid(row=0, column=3)
        lower_button_row_frame.columnconfigure(0, weight=1)
        lower_button_row_frame.columnconfigure(1, weight=1)
        lower_button_row_frame.columnconfigure(2, weight=1)
        lower_button_row_frame.columnconfigure(3, weight=1)

        self.root.after(100, self.update_time)

    def run(self):
        self.root.mainloop()

    def reset(self):
        self.start_datetime = None
        self.resync_datetime = None
        self.last_time_step = None
        self.total_time = 0
        self.current_activity = None
        self.paused = False
        self.started = False
        self.right_button.config(text="Stopped")
        self.right_button["state"] = tk.DISABLED
        self.left_button.config(text="Start")
        self.left_button["state"] = tk.NORMAL
        self.time_text.config(text="00:00:00")

    def update_time(self):
        if self.started and not self.paused:
            current_time_step = time.time()
            time_diff = current_time_step - self.last_time_step
            self.last_time_step = current_time_step
            self.total_time += time_diff
            self.time_text.config(text=time.strftime("%H:%M:%S", time.gmtime(self.total_time)))
            print(f"time:     {self.total_time}")
            time_diff_datetime = datetime.datetime.now() - self.start_datetime
            print(f"datetime: {time_diff_datetime.total_seconds()}")
            print(f"diff: {self.total_time - time_diff_datetime.total_seconds()}\n")
        self.root.after(100, self.update_time)

    def add_history_time_element(self, index, start_time, end_time, total_time):
        row_frame = tk.Frame(self.list_frame, height=20, width=1000)
        start_time_label = tk.Label(row_frame, text=start_time)
        end_time_label = tk.Label(row_frame, text=end_time)
        total_time_label = tk.Label(row_frame, text=total_time)
        row_frame.grid(row=index)
        row_frame.grid_propagate(False)
        self.list_frame.columnconfigure(0, weight=1)
        start_time_label.grid(row=0, column=0)
        end_time_label.grid(row=0, column=1)
        total_time_label.grid(row=0, column=2)
        row_frame.columnconfigure(0, weight=1)
        row_frame.columnconfigure(1, weight=1)
        row_frame.columnconfigure(2, weight=1)

    def project_menu_change(self, *args):
        print(self.project_menu_var.get())

    def task_menu_change(self, *args):
        print(self.task_menu_var.get())

    def start_action_resume_action(self):
        if not self.paused:
            current_time = datetime.datetime.now()
            self.start_datetime = current_time
            current_time_step = time.time()
            self.last_time_step = current_time_step
            self.started = True
            self.right_button.config(text="Stop")
            self.right_button["state"] = tk.NORMAL
            self.left_button["state"] = tk.DISABLED
        else:
            current_time_step = time.time()
            self.last_time_step = current_time_step
            self.paused = False
            self.right_button.config(text="Stop")
            self.right_button["state"] = tk.NORMAL
            self.left_button.config(text="Start")
            self.left_button["state"] = tk.DISABLED

    def stop_action_save_action(self):
        if not self.paused:
            self.paused = True
            self.right_button.config(text="Save")
            self.right_button["state"] = tk.NORMAL
            self.left_button.config(text="Resume")
            self.left_button["state"] = tk.NORMAL
            current_time_step = time.time()
            time_diff = current_time_step - self.last_time_step
            self.last_time_step = current_time_step
            self.resync_datetime = datetime.datetime.now()
            self.total_time += time_diff
        else:
            with open(self.config_file_path, "w+") as config_file:
                total_time_delta = datetime.timedelta(seconds=self.total_time)
                start_time = self.start_datetime.strftime("%-d %B %Y, %I:%M:%S%p")
                end_time = datetime.datetime.now().strftime("%-d %B %Y, %I:%M:%S%p")
                total_time = f"{total_time_delta.days}:{time.strftime('%H:%M:%S', time.gmtime(total_time_delta.seconds))}"
                self.time_history_list.append({"start_time": start_time,
                                               "end_time": end_time,
                                               "total_time": total_time,
                                               "user": None})
                # TODO add user
                self.add_history_time_element(len(self.time_history_list) - 1, start_time, end_time, total_time)
                json.dump({"time_history": self.time_history_list},
                          config_file)
            self.reset()

    def quit_action(self):
        with open(self.config_file_path, "w+") as config_file:
            json.dump({"time_history": self.time_history_list},
                      config_file)
        self.root.quit()
