import time
import datetime
import pyglet
import tkinter as tk

from tkinter.font import Font


class TimeTracker:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.last_time_step = None
        self.total_time = 0
        self.current_activity = None
        self.paused = False
        self.started = False

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

        self.current_activity_input = tk.Entry(self.root,
                                               bg=primary_color,
                                               highlightthickness=1,
                                               highlightbackground=button_hl_color,
                                               font=("", 15),
                                               width=73)
        upper_button_frame = tk.Frame(self.root,
                                      background=primary_color,
                                      highlightbackground=button_hl_color,
                                      highlightthickness=1,
                                      )
        self.left_button = tk.Button(upper_button_frame,
                                     bg=button_bg_color, foreground=button_fg_color,
                                     highlightthickness=1,
                                     highlightbackground=button_hl_color,
                                     text="Start", font=button_font,
                                     padx=180, pady=5,
                                     command=self.start_action_resume_action)
        self.right_button = tk.Button(upper_button_frame,
                                      bg=button_bg_color, foreground=button_fg_color,
                                      highlightthickness=1,
                                      highlightbackground=button_hl_color,
                                      text="Stopped", font=button_font,
                                      padx=180, pady=5,
                                      command=self.stop_action)
        self.right_button["state"] = tk.DISABLED

        self.list_frame = tk.Frame(self.root,
                                   background=primary_color,
                                   highlightbackground=button_hl_color,
                                   highlightthickness=1,
                                   height=170, width=880)

        list_button_frame = tk.Frame(self.root,
                                     background=primary_color,
                                     highlightbackground=button_hl_color,
                                     highlightthickness=1,
                                     )
        self.list_delete_button = tk.Button(list_button_frame,
                                            bg=button_bg_color, foreground=button_fg_color,
                                            highlightthickness=1,
                                            highlightbackground=button_hl_color,
                                            text="Delete", font=button_font,
                                            padx=75, pady=5)
        self.list_delete_button["state"] = tk.DISABLED
        self.list_edit_button = tk.Button(list_button_frame, foreground=button_fg_color,
                                          bg=button_bg_color,
                                          highlightthickness=1,
                                          highlightbackground=button_hl_color,
                                          text="Edit", font=button_font,
                                          padx=75, pady=5)
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
                                         padx=70, pady=5)
        self.about_button = tk.Button(lower_button_row_frame, foreground=button_fg_color,
                                      bg=button_bg_color,
                                      highlightthickness=1,
                                      highlightbackground=button_hl_color,
                                      text="About", font=button_font,
                                      padx=70, pady=5)
        self.help_button = tk.Button(lower_button_row_frame,
                                     bg=button_bg_color, foreground=button_fg_color,
                                     highlightthickness=1,
                                     highlightbackground=button_hl_color,
                                     text="Help", font=button_font,
                                     padx=70, pady=5)
        self.quit_button = tk.Button(lower_button_row_frame,
                                     bg=button_bg_color, foreground=button_fg_color,
                                     highlightthickness=1,
                                     highlightbackground=button_hl_color,
                                     text="Quit", font=button_font,
                                     padx=70, pady=5,
                                     command=self.quit_action)

        # layout
        time_frame.pack(expand=True)
        self.time_text.pack()

        self.current_activity_input.pack(expand=True)

        upper_button_frame.pack(expand=True)
        self.left_button.grid(row=0, column=0, padx=10, pady=5)
        self.right_button.grid(row=0, column=1, padx=10, pady=5)

        self.list_frame.pack(expand=True)

        list_button_frame.pack(expand=True)
        self.list_delete_button.grid(row=0, column=1, padx=0, pady=5)
        self.list_edit_button.grid(row=0, column=2, padx=0, pady=5)

        lower_button_row_frame.pack(expand=True)
        self.settings_button.grid(row=0, column=0, padx=0, pady=10)
        self.about_button.grid(row=0, column=1, padx=0, pady=10)
        self.help_button.grid(row=0, column=2, padx=0, pady=10)
        self.quit_button.grid(row=0, column=3, padx=0, pady=10)

        # self.root.grid_columnconfigure(0, weight=1)
        # self.root.grid_columnconfigure(4, weight=1)
        self.root.after(100, self.update_time)

    def run(self):
        self.root.mainloop()

    def reset(self):
        self.start_time = None
        self.end_time = None
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
        self.root.after(100, self.update_time)

    def start_action_resume_action(self):
        if not self.paused:
            current_time = datetime.datetime.now()
            self.start_time = current_time
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

    def stop_action(self):
        if not self.paused:
            self.paused = True
            self.right_button.config(text="Save")
            self.right_button["state"] = tk.NORMAL
            self.left_button.config(text="Resume")
            self.left_button["state"] = tk.NORMAL
            current_time_step = time.time()
            time_diff = current_time_step - self.last_time_step
            self.last_time_step = current_time_step
            self.total_time += time_diff
        else:
            # TODO save!
            self.reset()

    def quit_action(self):
        # TODO save before quiting
        self.root.quit()
