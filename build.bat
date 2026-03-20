@echo off
echo Building CMM Dashboard...
echo.

call venv\Scripts\activate

pyinstaller --noconfirm --onefile --windowed ^
    --name "CMM_Dashboard" ^
    --add-data "src;src" ^
    --add-data "templates;templates" ^
    --add-data "static;static" ^
    --add-data "app.py;." ^
    --add-data "gui.py;." ^
    --add-data "gui_single.py;." ^
    --add-data "gui_trend.py;." ^
    --add-data "gui_settings.py;." ^
    --add-data "gui_live.py;." ^
    --add-data "settings.json;." ^
    --hidden-import PyQt6 ^
    --hidden-import PyQt6.QtWebEngineWidgets ^
    --hidden-import PyQt6.QtWebEngineCore ^
    --hidden-import flask ^
    --hidden-import pandas ^
    --hidden-import plotly ^
    --hidden-import openpyxl ^
    --hidden-import watchdog ^
    --hidden-import statistics ^
    --collect-all PyQt6 ^
    --collect-all flask ^
    --collect-all jinja2 ^
    --collect-all werkzeug ^
    launcher.py

echo.
echo Done! Your executable is in the dist\ folder.
pause