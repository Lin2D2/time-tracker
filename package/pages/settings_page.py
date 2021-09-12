import tkinter as tk


class Settings(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent.root, width=2000, height=2000, bg=parent.primary_color)
        self.config_file_path = parent.config_file_path

        self.primary_color = parent.primary_color
        self.button_bg_color = parent.button_bg_color
        self.button_hl_color = parent.button_hl_color
        self.button_fg_color = parent.button_fg_color

        self.button_font = parent.button_font

        self.time_history_list = parent.time_history_list

        self.project_menu_items = parent.project_menu_items
        self.task_menu_items = parent.task_menu_items

        self.draw_home = parent.draw_home
        self.clear_root = parent.clear_root

        self.settings_label = tk.Label(self,
                                       text="Settings",
                                       highlightthickness=1,
                                       bg=self.primary_color,
                                       highlightbackground=self.primary_color,
                                       foreground="white",
                                       font=self.button_font)

    def draw(self):
        self.settings_label.pack()
