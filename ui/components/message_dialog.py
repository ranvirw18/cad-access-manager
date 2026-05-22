import customtkinter as ctk


def show_message(parent, title: str, message: str, icon: str = "info"):
    """Simple modal for errors and success."""
    dialog = ctk.CTkToplevel(parent)
    dialog.title(title)
    dialog.geometry("360x180")
    dialog.transient(parent)
    dialog.grab_set()

    color = "#e74c3c" if icon == "error" else "#2ecc71" if icon == "success" else "#3498db"
    ctk.CTkLabel(dialog, text=title, font=ctk.CTkFont(size=16, weight="bold"), text_color=color).pack(pady=(20, 8))
    ctk.CTkLabel(dialog, text=message, wraplength=320).pack(pady=8, padx=20)
    ctk.CTkButton(dialog, text="OK", command=dialog.destroy, width=100).pack(pady=16)

    dialog.update_idletasks()
    x = parent.winfo_x() + (parent.winfo_width() // 2) - 180
    y = parent.winfo_y() + (parent.winfo_height() // 2) - 90
    dialog.geometry(f"+{x}+{y}")
