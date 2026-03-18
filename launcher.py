# launcher.py
# Entry point for the packaged .exe
# Starts Streamlit and opens the browser automatically.

import sys
import os
import subprocess
import webbrowser
import time
import threading


def open_browser():
    """Wait for Streamlit to start then open the browser."""
    time.sleep(4)
    webbrowser.open("http://localhost:8501")


def main():
    # This flag prevents the infinite loop on Windows
    if os.environ.get("CMM_DASHBOARD_RUNNING"):
        return

    os.environ["CMM_DASHBOARD_RUNNING"] = "1"

    # Find app.py whether running as .exe or script
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    app_path = os.path.join(base_path, "app.py")

    # Open browser in background
    threading.Thread(target=open_browser, daemon=True).start()

    # Start Streamlit
    os.system(
        f'streamlit run "{app_path}" '
        f'--server.headless true '
        f'--server.port 8501 '
        f'--browser.gatherUsageStats false'
    )


if __name__ == "__main__":
    main()
