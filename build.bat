@echo off
echo Building CMM Dashboard...
echo.

call venv\Scripts\activate

pyinstaller --noconfirm --onefile --windowed ^
    --name "CMM_Dashboard" ^
    --add-data "app.py;." ^
    --add-data "templates;templates" ^
    --add-data "static;static" ^
    --add-data "src;src" ^
    --hidden-import flask ^
    --hidden-import pandas ^
    --hidden-import plotly ^
    --hidden-import statistics ^
    --collect-all flask ^
    --collect-all jinja2 ^
    --collect-all werkzeug ^
    launcher.py

echo.
echo Done! Your executable is in the dist\ folder.
pause