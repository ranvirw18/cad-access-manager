"""
Admin panel — manage students (add, remove, password, extend, disable).
"""

from datetime import date

import customtkinter as ctk

from services.admin_service import AdminService
from ui.components.message_dialog import show_message
from utils.dates import days_remaining, is_expired


class AdminWindow(ctk.CTkFrame):
    def __init__(self, master, on_back, **kwargs):
        super().__init__(master, **kwargs)
        self.admin_service = AdminService()
        self._on_back = on_back
        self._logged_in = False
        self._build_login_ui()

    def _build_login_ui(self):
        for w in self.winfo_children():
            w.destroy()
        ctk.CTkLabel(self, text="Admin Login", font=ctk.CTkFont(size=20, weight="bold")).pack(
            pady=(40, 16)
        )
        self.admin_user = ctk.CTkEntry(self, placeholder_text="Admin username", width=260, height=38)
        self.admin_user.pack(pady=6)
        self.admin_pass = ctk.CTkEntry(
            self, placeholder_text="Password", show="*", width=260, height=38
        )
        self.admin_pass.pack(pady=6)
        ctk.CTkButton(self, text="Login", width=260, command=self._admin_login).pack(pady=16)
        ctk.CTkButton(
            self, text="Back to Student Login", fg_color="transparent", border_width=1, command=self._on_back
        ).pack(pady=8)

    def _admin_login(self):
        admin = self.admin_service.login_admin(
            self.admin_user.get().strip(), self.admin_pass.get()
        )
        if not admin:
            show_message(self.winfo_toplevel(), "Access denied", "Invalid admin credentials.", "error")
            return
        self._logged_in = True
        self._build_dashboard()

    def _build_dashboard(self):
        for w in self.winfo_children():
            w.destroy()

        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=16, pady=(12, 0))
        ctk.CTkLabel(top, text="Student Management", font=ctk.CTkFont(size=18, weight="bold")).pack(
            side="left"
        )
        ctk.CTkButton(top, text="Refresh", width=80, command=self._refresh_list).pack(side="right")
        ctk.CTkButton(top, text="Logout", width=80, command=self._build_login_ui).pack(side="right", padx=8)

        self.list_frame = ctk.CTkScrollableFrame(self, width=440, height=220)
        self.list_frame.pack(pady=12, padx=16)

        form = ctk.CTkFrame(self)
        form.pack(pady=8, padx=16, fill="x")
        ctk.CTkLabel(form, text="Add student").grid(row=0, column=0, columnspan=3, pady=(8, 4), sticky="w", padx=8)
        self.new_user = ctk.CTkEntry(form, placeholder_text="Username", width=130)
        self.new_user.grid(row=1, column=0, padx=4, pady=4)
        self.new_pass = ctk.CTkEntry(form, placeholder_text="Password", show="*", width=130)
        self.new_pass.grid(row=1, column=1, padx=4, pady=4)
        ctk.CTkButton(form, text="Add (50 days)", width=120, command=self._add_student).grid(
            row=1, column=2, padx=4, pady=4
        )

        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.pack(pady=8)
        ctk.CTkLabel(actions, text="Selected student ID:").pack(side="left", padx=4)
        self.selected_id = ctk.CTkEntry(actions, width=60)
        self.selected_id.pack(side="left", padx=4)
        ctk.CTkButton(actions, text="+30 days", width=90, command=lambda: self._extend(30)).pack(
            side="left", padx=4
        )
        ctk.CTkButton(actions, text="Disable", width=80, command=lambda: self._toggle_active(False)).pack(
            side="left", padx=4
        )
        ctk.CTkButton(actions, text="Enable", width=80, command=lambda: self._toggle_active(True)).pack(
            side="left", padx=4
        )
        ctk.CTkButton(actions, text="New password", width=100, command=self._change_password).pack(
            side="left", padx=4
        )
        ctk.CTkButton(actions, text="Remove", width=80, fg_color="#c0392b", command=self._remove_student).pack(
            side="left", padx=4
        )

        ctk.CTkButton(self, text="Back to Student Login", command=self._on_back).pack(pady=12)
        self._refresh_list()

    def _refresh_list(self):
        for w in self.list_frame.winfo_children():
            w.destroy()
        students = self.admin_service.list_students()
        if not students:
            ctk.CTkLabel(self.list_frame, text="No students yet.").pack(anchor="w", padx=8, pady=4)
            return
        for s in students:
            expired = is_expired(s.expiry_date)
            status = "EXPIRED" if expired else f"{days_remaining(s.expiry_date)}d left"
            active = "ON" if s.is_active else "OFF"
            line = (
                f"ID {s.id} | {s.username} | join {s.join_date} | "
                f"expires {s.expiry_date} | {status} | active {active}"
            )
            ctk.CTkLabel(self.list_frame, text=line, anchor="w").pack(fill="x", padx=8, pady=2)

    def _add_student(self):
        u, p = self.new_user.get().strip(), self.new_pass.get()
        if not u or not p:
            show_message(self.winfo_toplevel(), "Error", "Username and password required.", "error")
            return
        try:
            s = self.admin_service.add_student(u, p)
            show_message(
                self.winfo_toplevel(),
                "Student added",
                f"{s.username}\nJoin: {s.join_date}\nExpires: {s.expiry_date}",
                "success",
            )
            self.new_user.delete(0, "end")
            self.new_pass.delete(0, "end")
            self._refresh_list()
        except Exception as e:
            show_message(self.winfo_toplevel(), "Error", str(e), "error")

    def _get_selected_id(self) -> int | None:
        try:
            return int(self.selected_id.get().strip())
        except ValueError:
            show_message(self.winfo_toplevel(), "Error", "Enter a valid student ID from the list.", "error")
            return None

    def _extend(self, days: int):
        sid = self._get_selected_id()
        if sid is None:
            return
        try:
            self.admin_service.extend_validity(sid, days)
            show_message(self.winfo_toplevel(), "Extended", f"Added {days} days to expiry.", "success")
            self._refresh_list()
        except Exception as e:
            show_message(self.winfo_toplevel(), "Error", str(e), "error")

    def _toggle_active(self, active: bool):
        sid = self._get_selected_id()
        if sid is None:
            return
        self.admin_service.set_account_active(sid, active)
        show_message(self.winfo_toplevel(), "Updated", "Account status changed.", "success")
        self._refresh_list()

    def _change_password(self):
        sid = self._get_selected_id()
        if sid is None:
            return
        dialog = ctk.CTkInputDialog(text="New password:", title="Change password")
        new_p = dialog.get_input()
        if not new_p:
            return
        self.admin_service.change_password(sid, new_p)
        show_message(self.winfo_toplevel(), "Updated", "Password changed.", "success")

    def _remove_student(self):
        sid = self._get_selected_id()
        if sid is None:
            return
        self.admin_service.remove_student(sid)
        show_message(self.winfo_toplevel(), "Removed", "Student deleted.", "success")
        self._refresh_list()
