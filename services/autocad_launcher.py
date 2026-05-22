"""
Launch AutoCAD after a successful student login.
"""

import subprocess
from pathlib import Path

from config.settings import AUTOCAD_EXE


class AutoCADLauncher:
    def __init__(self, exe_path: str | None = None):
        self.exe_path = Path(exe_path or AUTOCAD_EXE)

    def is_installed(self) -> bool:
        return self.exe_path.is_file()

    def launch(self) -> None:
        if not self.is_installed():
            raise FileNotFoundError(
                f"AutoCAD not found at:\n{self.exe_path}\n"
                "Update AUTOCAD_EXE in config/settings.py"
            )
        subprocess.Popen([str(self.exe_path)], shell=False)
