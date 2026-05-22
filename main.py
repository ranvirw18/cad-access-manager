"""
CAD Institute Launcher — entry point.

Run:  python main.py
"""

from ui.app import CadLauncherApp


def main():
    app = CadLauncherApp()
    app.mainloop()


if __name__ == "__main__":
    main()
