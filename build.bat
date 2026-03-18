@echo off
echo Building CMM Dashboard...
echo.

call venv\Scripts\activate

pyinstaller --noconfirm --windowed ^
    --name "CMM_Dashboard" ^
    --add-data "app.py;." ^
    --add-data "models.py;." ^
    --add-data "parser.py;." ^
    --add-data "evaluator.py;." ^
    --add-data "visualizer.py;." ^
    --add-data "trend.py;." ^
    --add-data "capability.py;." ^
    --hidden-import streamlit ^
    --hidden-import streamlit.web.cli ^
    --hidden-import streamlit.runtime ^
    --hidden-import pandas ^
    --hidden-import plotly ^
    --hidden-import statistics ^
    --collect-all streamlit ^
    launcher.py

echo.
echo Done! Your app is in the dist\CMM_Dashboard folder.
pause
