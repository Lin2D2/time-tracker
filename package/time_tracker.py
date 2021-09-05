import datetime
import pyglet
import tkinter as tk

from tkinter.font import Font


class TimeTracker:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.total_time = None
        self.current_activity = None
        self.paused = False
        self.started = False

        # UI
        self.root = tk.Tk()
        self.root.title("Time Tracker")
        self.root.geometry("950x500")

        # TODO not working
        pyglet.font.add_directory('resources')
        time_font = Font(family="DSEG7 Classic", size=70, weight="bold")

        # definition
        time_frame = tk.Frame(self.root,
                              highlightthickness=1,
                              highlightbackground="#323232")

        time_text = tk.Text(time_frame,
                            highlightthickness=1,
                            highlightbackground="#323232",
                            height=1, width=14,
                            font=time_font)
        time_text.insert(tk.END, "00:00:00")
        time_text.config(state=tk.DISABLED)
        time_text.tag_configure("center", justify='center')
        time_text.tag_add("center", "1.0", "end")

        current_activity_input = tk.Entry(self.root,
                                          highlightthickness=1,
                                          highlightbackground="#505050",
                                          font=("", 15),
                                          width=73)

        left_button = tk.Button(self.root,
                                bg="#414141",
                                highlightthickness=1,
                                highlightbackground="#505050",
                                text="Start", font=("", 13),
                                padx=180, pady=5)
        right_button = tk.Button(self.root,
                                 bg="#414141",
                                 highlightthickness=1,
                                 highlightbackground="#505050",
                                 text="Stopped", font=("", 13),
                                 padx=180, pady=5)

        list_frame = tk.Frame(self.root,
                              highlightbackground="#505050",
                              highlightthickness=1,
                              height=170, width=880)

        list_delete_button = tk.Button(self.root,
                                       bg="#414141",
                                       highlightthickness=1,
                                       highlightbackground="#505050",
                                       text="Delete", font=("", 13),
                                       padx=75, pady=5)
        list_edit_button = tk.Button(self.root,
                                     bg="#414141",
                                     highlightthickness=1,
                                     highlightbackground="#505050",
                                     text="Edit", font=("", 13),
                                     padx=75, pady=5)

        settings_button = tk.Button(self.root,
                                    bg="#414141",
                                    highlightthickness=1,
                                    highlightbackground="#505050",
                                    text="Settings", font=("", 13),
                                    padx=70, pady=5)
        about_button = tk.Button(self.root,
                                 bg="#414141",
                                 highlightthickness=1,
                                 highlightbackground="#505050",
                                 text="About", font=("", 13),
                                 padx=70, pady=5)
        help_button = tk.Button(self.root,
                                bg="#414141",
                                highlightthickness=1,
                                highlightbackground="#505050",
                                text="Help", font=("", 13),
                                padx=70, pady=5)
        quit_button = tk.Button(self.root,
                                bg="#414141",
                                highlightthickness=1,
                                highlightbackground="#505050",
                                text="Quit", font=("", 13),
                                padx=70, pady=5)

        # layout
        time_text.pack()
        time_frame.grid(row=0, column=0, columnspan=4, padx=10, pady=5)
        current_activity_input.grid(row=1, column=0, columnspan=4, padx=10, pady=5)
        left_button.grid(row=2, column=0, padx=10, columnspan=2, pady=5)
        right_button.grid(row=2, column=2, padx=10, columnspan=2, pady=5)
        list_frame.grid(row=3, column=0, columnspan=4, padx=10, pady=10)
        list_delete_button.grid(row=4, column=2, padx=0, pady=5)
        list_edit_button.grid(row=4, column=3, padx=0, pady=5)
        settings_button.grid(row=5, column=0, padx=0, pady=10)
        about_button.grid(row=5, column=1, padx=0, pady=10)
        help_button.grid(row=5, column=2, padx=0, pady=10)
        quit_button.grid(row=5, column=3, padx=0, pady=10)

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(4, weight=1)

    def run(self):
        self.root.mainloop()
