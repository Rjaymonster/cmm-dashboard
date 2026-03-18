import sys
import os
import threading
import webbrowser
import time
from flask import Flask

def open_browser():
    time.sleep(2)
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    # Find correct base path whether running as .exe or script
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    # Set working directory so Flask finds templates and static
    os.chdir(base_path)

    # Add src to path
    sys.path.insert(0, os.path.join(base_path, "src"))

    # Open browser after short delay
    threading.Thread(target=open_browser, daemon=True).start()

    # Import and run the Flask app
    from app import app
    app.run(debug=False, port=5000)