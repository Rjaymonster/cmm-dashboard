@echo off
title CMM Dashboard
echo Starting CMM Dashboard...
echo.
echo Please wait — your browser will open automatically.
echo Keep this window open while using the app.
echo Close this window to stop the app.
echo.

cd /d "%~dp0"
call venv\Scripts\activate
streamlit run app.py --browser.gatherUsageStats false

pause
