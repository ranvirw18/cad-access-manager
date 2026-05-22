"""
Application settings — change paths here for your institute PCs.
"""

import sys
from pathlib import Path

# When built as .exe, store data next to the executable (not in temp folder)
if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

# SQLite database file (created automatically on first run)
DATABASE_PATH = BASE_DIR / "data" / "cad_launcher.db"

# Default subscription length in days
ACCESS_DAYS = 50

# AutoCAD executable — update this path on each lab PC if needed
AUTOCAD_EXE = r"C:\Program Files\Autodesk\AutoCAD 2024\acad.exe"

# Default admin account (created only when database is empty)
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"  # Change immediately after first login

# UI
APP_TITLE = "CAD Institute Launcher"
WINDOW_SIZE = "480x520"
THEME = "dark"
COLOR_THEME = "blue"
