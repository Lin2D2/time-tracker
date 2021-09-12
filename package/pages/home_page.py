import time
import datetime
import json
import tkinter as tk


class Home(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent.root, width=2000, height=2000, bg=parent.primary_color)
        self.config_file_path = parent.config_file_path

        self.primary_color = parent.primary_color
        self.button_bg_color = parent.button_bg_color
        self.button_hl_color = parent.button_hl_color
        self.button_fg_color = parent.button_fg_color

        self.time_font = parent.time_font
        self.button_font = parent.button_font

        self.start_datetime = None
        self.resync_datetime = None
        self.last_time_step = None
        self.total_time = 0
        self.current_activity = None
        self.paused = False
        self.started = False

        self.time_history_list = parent.time_history_list

        self.project_menu_items = parent.project_menu_items
        self.task_menu_items = parent.task_menu_items

        self.draw_settings = parent.draw_settings
        self.clear_root = parent.clear_root

        self.time_frame = tk.Frame(self,
                                   bg=self.primary_color,
                                   highlightthickness=1,
                                   highlightbackground=self.primary_color)

        self.time_text = tk.Label(self.time_frame,
                                  text="00:00:00",
                                  highlightthickness=1,
                                  bg=self.primary_color,
                                  highlightbackground=self.primary_color,
                                  foreground="white",
                                  height=1, width=14,
                                  font=self.time_font)

        # self.current_activity_input = tk.Entry(self.root,
        #                                        bg=primary_color,
        #                                        highlightthickness=1,
        #                                        highlightbackground=button_hl_color,
        #                                        font=("", 15),
        #                                        width=73)
        self.activity_input_frame = tk.Frame(self,
                                             bg=self.primary_color,
                                             highlightthickness=1,
                                             highlightbackground=self.primary_color)
        self.activity_input_project_menu_frame = tk.Frame(self.activity_input_frame,
                                                          bg=self.primary_color,
                                                          highlightthickness=1,
                                                          highlightbackground=self.primary_color)
        self.activity_input_project_menu_label = tk.Label(self.activity_input_project_menu_frame,
                                                          text="Project:",
                                                          highlightthickness=1,
                                                          bg=self.primary_color,
                                                          highlightbackground=self.primary_color,
                                                          foreground="white",
                                                          font=self.button_font)
        self.project_menu_var = tk.Variable(self)
        if len(self.project_menu_items) < 1:
            self.project_menu_var.set("Unset")
        else:
            self.project_menu_var.set(self.project_menu_items[0])
        self.project_menu_var.trace("w", self.project_menu_change)
        self.activity_input_project_menu = tk.OptionMenu(self.activity_input_project_menu_frame,
                                                         self.project_menu_var,
                                                         self.project_menu_items)
        self.activity_input_project_menu.config(highlightthickness=1,
                                                bg=self.primary_color,
                                                highlightbackground=self.primary_color,
                                                foreground="white",
                                                font=self.button_font,
                                                width=30,
                                                anchor='w')
        self.activity_input_task_menu_frame = tk.Frame(self.activity_input_frame,
                                                       bg=self.primary_color,
                                                       highlightthickness=1,
                                                       highlightbackground=self.primary_color)
        self.activity_input_task_menu_label = tk.Label(self.activity_input_task_menu_frame,
                                                       text="Task:",
                                                       highlightthickness=1,
                                                       bg=self.primary_color,
                                                       highlightbackground=self.primary_color,
                                                       foreground="white",
                                                       font=self.button_font)
        self.task_menu_var = tk.Variable(self)
        if len(self.task_menu_items) < 1:
            self.task_menu_var.set("Unset")
        else:
            self.task_menu_var.set(self.task_menu_items[0])
        self.task_menu_var.trace("w", self.task_menu_change)
        self.activity_input_task_menu = tk.OptionMenu(self.activity_input_task_menu_frame,
                                                      self.task_menu_var,
                                                      self.task_menu_items)
        self.activity_input_task_menu.config(highlightthickness=1,
                                             bg=self.primary_color,
                                             highlightbackground=self.primary_color,
                                             foreground="white",
                                             font=self.button_font,
                                             width=30,
                                             anchor='w')

        self.upper_button_frame = tk.Frame(self,
                                           background=self.primary_color,
                                           highlightbackground=self.button_hl_color,
                                           highlightthickness=1)
        self.left_button = tk.Button(self.upper_button_frame,
                                     bg=self.button_bg_color, foreground=self.button_fg_color,
                                     highlightthickness=1,
                                     highlightbackground=self.button_hl_color,
                                     text="Start", font=self.button_font,
                                     padx=350, pady=5,
                                     command=self.start_action_resume_action)
        self.right_button = tk.Button(self.upper_button_frame,
                                      bg=self.button_bg_color, foreground=self.button_fg_color,
                                      highlightthickness=1,
                                      highlightbackground=self.button_hl_color,
                                      text="Stopped", font=self.button_font,
                                      padx=350, pady=5,
                                      command=self.stop_action_save_action)
        self.right_button["state"] = tk.DISABLED

        self.list_frame = tk.Frame(self,
                                   background=self.primary_color,
                                   highlightbackground=self.button_hl_color,
                                   highlightthickness=1,
                                   height=230, width=880)

        self.list_button_frame_frame = tk.Frame(self,
                                                background=self.primary_color,
                                                highlightbackground=self.button_hl_color,
                                                highlightthickness=1,
                                                )
        self.list_button_frame = tk.Frame(self.list_button_frame_frame,
                                          background=self.primary_color,
                                          highlightbackground=self.button_hl_color,
                                          highlightthickness=1,
                                          )
        self.list_delete_button = tk.Button(self.list_button_frame,
                                            bg=self.button_bg_color, foreground=self.button_fg_color,
                                            highlightthickness=1,
                                            highlightbackground=self.button_hl_color,
                                            text="Delete", font=self.button_font,
                                            padx=130, pady=5)
        self.list_delete_button["state"] = tk.DISABLED
        self.list_edit_button = tk.Button(self.list_button_frame, foreground=self.button_fg_color,
                                          bg=self.button_bg_color,
                                          highlightthickness=1,
                                          highlightbackground=self.button_hl_color,
                                          text="Edit", font=self.button_font,
                                          padx=130, pady=5)
        self.list_edit_button["state"] = tk.DISABLED

        self.lower_button_row_frame = tk.Frame(self,
                                               background=self.primary_color,
                                               highlightbackground=self.button_hl_color,
                                               highlightthickness=1,
                                               )
        self.settings_button = tk.Button(self.lower_button_row_frame, foreground=self.button_fg_color,
                                         bg=self.button_bg_color,
                                         highlightthickness=1,
                                         highlightbackground=self.button_hl_color,
                                         text="Settings", font=self.button_font,
                                         padx=150, pady=5,
                                         command=self.settings_action)
        self.about_button = tk.Button(self.lower_button_row_frame, foreground=self.button_fg_color,
                                      bg=self.button_bg_color,
                                      highlightthickness=1,
                                      highlightbackground=self.button_hl_color,
                                      text="About", font=self.button_font,
                                      padx=150, pady=5)
        self.help_button = tk.Button(self.lower_button_row_frame,
                                     bg=self.button_bg_color, foreground=self.button_fg_color,
                                     highlightthickness=1,
                                     highlightbackground=self.button_hl_color,
                                     text="Help", font=self.button_font,
                                     padx=150, pady=5)
        self.quit_button = tk.Button(self.lower_button_row_frame,
                                     bg=self.button_bg_color, foreground=self.button_fg_color,
                                     highlightthickness=1,
                                     highlightbackground=self.button_hl_color,
                                     text="Quit", font=self.button_font,
                                     padx=150, pady=5,
                                     command=self.quit_action)

        self.after(100, self.update_time)

    def draw(self):
        self.time_frame.pack(fill=tk.X)
        self.time_text.pack()

        # self.current_activity_input.pack(fill=tk.X)
        self.activity_input_frame.pack(fill=tk.X)
        self.activity_input_frame.columnconfigure(0, weight=1)
        self.activity_input_frame.columnconfigure(1, weight=1)
        self.activity_input_project_menu_frame.grid(row=0, column=0)
        self.activity_input_project_menu_label.grid(row=0, column=0)
        self.activity_input_project_menu.grid(row=0, column=1)
        self.activity_input_task_menu_frame.grid(row=0, column=1)
        self.activity_input_task_menu_label.grid(row=0, column=0)
        self.activity_input_task_menu.grid(row=0, column=1)

        self.upper_button_frame.pack(fill=tk.X)
        self.left_button.grid(row=0, column=0)
        self.right_button.grid(row=0, column=1)
        self.upper_button_frame.columnconfigure(0, weight=1)
        self.upper_button_frame.columnconfigure(1, weight=1)

        self.list_frame.pack(fill=tk.BOTH)
        self.list_frame.grid_propagate(False)
        for index, time_history in enumerate(self.time_history_list):
            self.add_history_time_element(index,
                                          time_history["start_time"],
                                          time_history["end_time"],
                                          time_history["total_time"])

        self.list_button_frame_frame.pack(fill=tk.X)
        self.list_button_frame_frame.columnconfigure(0, weight=1)
        self.list_button_frame_frame.columnconfigure(1, weight=0)
        self.list_button_frame.grid(row=0, column=1)
        self.list_button_frame.columnconfigure(0, weight=1)
        self.list_button_frame.columnconfigure(1, weight=1)
        self.list_delete_button.grid(row=0, column=0)
        self.list_edit_button.grid(row=0, column=1)

        self.lower_button_row_frame.pack(fill=tk.X)
        self.settings_button.grid(row=0, column=0)
        self.about_button.grid(row=0, column=1)
        self.help_button.grid(row=0, column=2)
        self.quit_button.grid(row=0, column=3)
        self.lower_button_row_frame.columnconfigure(0, weight=1)
        self.lower_button_row_frame.columnconfigure(1, weight=1)
        self.lower_button_row_frame.columnconfigure(2, weight=1)
        self.lower_button_row_frame.columnconfigure(3, weight=1)

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
        self.after(100, self.update_time)

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

    def settings_action(self):
        self.clear_root()
        self.draw_settings()

    def quit_action(self):
        with open(self.config_file_path, "w+") as config_file:
            json.dump({"time_history": self.time_history_list},
                      config_file)
        self.quit()
