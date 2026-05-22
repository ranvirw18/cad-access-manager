"""
Student login screen — launches AutoCAD when checks pass.
"""

import customtkinter as ctk

from config.settings import APP_TITLE
from services.auth_service import AuthService, LoginStatus
from services.autocad_launcher import AutoCADLauncher
from ui.components.message_dialog import show_message


class LoginWindow(ctk.CTkFrame):
    def __init__(self, master, on_admin_click, **kwargs):
        super().__init__(master, **kwargs)
        self.auth = AuthService()
        self.launcher = AutoCADLauncher()
        self._on_admin_click = on_admin_click
        self._build_ui()

    def _build_ui(self):
        ctk.CTkLabel(
            self,
            text=APP_TITLE,
            font=ctk.CTkFont(size=22, weight="bold"),
        ).pack(pady=(30, 4))
        ctk.CTkLabel(self, text="Student Login", text_color="gray").pack(pady=(0, 24))

        self.username = ctk.CTkEntry(self, placeholder_text="Username", width=280, height=40)
        self.username.pack(pady=8)
        self.password = ctk.CTkEntry(
            self, placeholder_text="Password", show="*", width=280, height=40
        )
        self.password.pack(pady=8)
        self.password.bind("<Return>", lambda _: self._on_login())

        ctk.CTkButton(
            self, text="Login & Launch AutoCAD", width=280, height=42, command=self._on_login
        ).pack(pady=20)

        ctk.CTkButton(
            self,
            text="Admin Panel",
            width=140,
            height=32,
            fg_color="transparent",
            border_width=1,
            command=self._on_admin_click,
        ).pack(pady=8)

    def _on_login(self):
        username = self.username.get().strip()
        password = self.password.get()
        if not username or not password:
            show_message(self.winfo_toplevel(), "Missing fields", "Enter username and password.", "error")
            return

        result = self.auth.login_student(username, password)

        if result.status == LoginStatus.USER_NOT_FOUND:
            show_message(self.winfo_toplevel(), "Login failed", "User does not exist.", "error")
        elif result.status == LoginStatus.WRONG_PASSWORD:
            show_message(self.winfo_toplevel(), "Login failed", "Incorrect password.", "error")
        elif result.status == LoginStatus.ACCOUNT_DISABLED:
            show_message(self.winfo_toplevel(), "Account disabled", "Contact your institute admin.", "error")
        elif result.status == LoginStatus.SUBSCRIPTION_EXPIRED:
            show_message(
                self.winfo_toplevel(),
                "Subscription Expired",
                "Your 50-day access has ended.\nPlease contact the institute to renew.",
                "error",
            )
        elif result.status == LoginStatus.SUCCESS:
            try:
                self.launcher.launch()
                show_message(
                    self.winfo_toplevel(),
                    "Welcome",
                    f"AutoCAD is starting.\nEnjoy your session, {username}!",
                    "success",
                )
                self.password.delete(0, "end")
            except FileNotFoundError as e:
                show_message(self.winfo_toplevel(), "AutoCAD not found", str(e), "error")
