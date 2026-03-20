# launcher.py
# Entry point for the packaged .exe
# Starts the PyQt6 desktop application.

import sys
import os


def main():
    # Set base path for bundled resources
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
        os.chdir(base_path)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    # Add src to path
    sys.path.insert(0, os.path.join(base_path, "src"))

    # Disable WebEngine sandbox for network drive compatibility
    os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"

    # Launch the PyQt6 app
    from gui import main as gui_main
    gui_main()


if __name__ == "__main__":
    main()