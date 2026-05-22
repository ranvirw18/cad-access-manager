"""
Main application window — switches between student login and admin panel.
"""

import customtkinter as ctk

from config.settings import APP_TITLE, COLOR_THEME, THEME, WINDOW_SIZE
from ui.admin_window import AdminWindow
from ui.login_window import LoginWindow


class CadLauncherApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode(THEME)
        ctk.set_default_color_theme(COLOR_THEME)
        self.title(APP_TITLE)
        self.geometry(WINDOW_SIZE)
        self.resizable(False, False)
        self._container = ctk.CTkFrame(self, fg_color="transparent")
        self._container.pack(fill="both", expand=True)
        self.show_login()

    def show_login(self):
        self._clear()
        LoginWindow(self._container, on_admin_click=self.show_admin).pack(fill="both", expand=True)

    def show_admin(self):
        self._clear()
        AdminWindow(self._container, on_back=self.show_login).pack(fill="both", expand=True)

    def _clear(self):
        for w in self._container.winfo_children():
            w.destroy()
