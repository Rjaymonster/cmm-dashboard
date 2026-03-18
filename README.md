# CMM Measurement Dashboard

A Python application for analyzing MODUS CMM inspection reports with 
interactive visualizations, trend analysis, and process capability studies.

## Features

- **Single Report Analysis** — parse MODUS CSV exports and visualize 
  feature deviations, tolerance consumption, and pass/fail status
- **GD&T Evaluation** — supports 14 feature types including MMC/LMC 
  bonus tolerance calculation
- **Multi-Run Trend Analysis** — upload multiple reports and track 
  deviation trends, feature stability, and pass rates over time
- **Process Capability** — automatic Cp/Cpk calculation with industry 
  standard ratings across 30+ runs
- **Interactive Charts** — built with Plotly, all charts are zoomable 
  and hoverable

## Supported GD&T Feature Types

Form, Orientation, Location, Runout, Profile, and Size tolerances 
including MMC and LMC bonus tolerance.

## Setup

1. Install Python 3.12+
2. Clone this repository
3. Create and activate a virtual environment:
```
   python -m venv venv
   venv\Scripts\activate
```
4. Install dependencies:
```
   pip install -r requirements.txt
```
5. Run the app:
```
   streamlit run app.py
```

Or double click `Launch CMM Dashboard.bat` on Windows.

## CSV Format

Your MODUS export should have these columns:
```
Feature Name, Feature Type, Nominal, Upper Tolerance, 
Lower Tolerance, Actual, Deviation
```

Optional MMC/LMC columns:
```
Material Condition, MMC/LMC Size, Actual Size
```

## Built With

- Python 3.12
- Pandas
- Plotly
- Streamlit