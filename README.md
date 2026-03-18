# CMM Measurement Dashboard

A standalone Windows application and web tool for analyzing MODUS CMM 
inspection reports with interactive visualizations, trend analysis, 
and process capability studies.

## Features

- **Single Report Analysis** — parse MODUS reports and visualize 
  feature deviations, tolerance consumption, and pass/fail status
- **GD&T Evaluation** — supports 14 feature types including MMC/LMC 
  bonus tolerance calculation
- **Multi-Run Trend Analysis** — upload multiple reports and track 
  deviation trends, feature stability, and pass rates over time
- **Process Capability** — automatic Cp/Cpk calculation with industry 
  standard ratings across 30+ runs
- **Interactive Charts** — built with Plotly, all charts are zoomable 
  and hoverable
- **Standalone .exe** — runs on any Windows machine with no Python 
  or setup required

## Supported Report Formats

- Standard CSV format with named columns
- MODUS fixed-format inspection reports (.csv or .txt)

## Supported GD&T Feature Types

| Category    | Types |
|-------------|-------|
| Form        | Circularity, Cylindricity, Flatness, Straightness |
| Orientation | Angularity, Parallelism, Perpendicularity |
| Location    | Position, Concentricity |
| Runout      | Runout, Total Runout |
| Profile     | Profile of a Line, Profile of a Surface |
| Size        | Diameter |

MMC and LMC bonus tolerance supported on Position, Straightness,
Perpendicularity, Parallelism, and Angularity.

## Running the App

### Option 1 — Standalone Executable (No Python Required)
Double click `CMM_Dashboard.exe` in the `dist/` folder.

### Option 2 — Run from Source
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Then open `http://127.0.0.1:5000` in your browser.

### Option 3 — Batch File
Double click `Launch CMM Dashboard.bat`

## Building the Executable
```
.\build.bat
```
Output will be in `dist\CMM_Dashboard.exe`

## CSV Format

Standard format:
```
Feature Name, Feature Type, Nominal, Upper Tolerance, 
Lower Tolerance, Actual, Deviation
```

With MMC/LMC:
```
Feature Name, Feature Type, Nominal, Upper Tolerance, 
Lower Tolerance, Actual, Deviation,
Material Condition, MMC/LMC Size, Actual Size
```

## Project Structure
```
cmm-dashboard/
├── src/               Python modules
├── templates/         Flask HTML templates  
├── static/            CSS styling
├── data/              Sample report files
├── app.py             Flask web application
├── launcher.py        Executable entry point
├── build.bat          Build script
└── requirements.txt   Dependencies
```

## Built With

Python 3.12 · Flask · Pandas · Plotly · PyInstaller

## Links

GitHub: https://github.com/Rjaymonster/cmm-dashboard