# parser.py
# Auto-detects report format and routes to the correct parser.
# Supports:
#   - Standard CSV format (Feature Name, Feature Type, Nominal...)
#   - MODUS fixed-format report (.csv or .txt)

import os
import pandas as pd
from models import Feature, Measurement, Tolerance, Report


def _is_modus_format(filepath: str) -> bool:
    """
    Peeks at the first few lines to determine if this is a
    MODUS fixed-format report rather than a standard CSV.
    """
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            first_lines = [f.readline().strip() for _ in range(3)]
        # MODUS reports start with PROGRAM TITLE and DATETIME
        # Standard CSVs start with Feature Name header
        return (
            not first_lines[0].startswith("Feature Name") and
            "ACTUAL" in first_lines[2] or
            "INSPECTION" in " ".join(first_lines)
        )
    except Exception:
        return False


def load_report(filepath: str) -> Report:
    ext = os.path.splitext(filepath)[1].lower()
    if ext in (".res", ".rtf") or _is_modus_format(filepath):
        from modus_parser import load_modus_report
        return load_modus_report(filepath)
    else:
        return _load_csv_report(filepath)


def _load_csv_report(filepath: str) -> Report:
    """
    Loads a standard CSV report with columns:
    Feature Name, Feature Type, Nominal, Upper Tolerance,
    Lower Tolerance, Actual, Deviation
    """
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find report file: {filepath}")

    df.columns = df.columns.str.strip()
    df.dropna(how="all", inplace=True)

    features = []

    for _, row in df.iterrows():
        tolerance = Tolerance(
            upper=float(row["Upper Tolerance"]),
            lower=float(row["Lower Tolerance"]),
        )

        measurement = Measurement(
            actual=float(row["Actual"]),
            deviation=float(row["Deviation"]),
        )

        material_condition = "RFS"
        mmc_lmc_size       = None
        actual_size        = None

        if "Material Condition" in df.columns:
            mc = row.get("Material Condition")
            if pd.notna(mc):
                material_condition = str(mc).strip()

        if "MMC/LMC Size" in df.columns:
            size = row.get("MMC/LMC Size")
            if pd.notna(size):
                mmc_lmc_size = float(size)

        if "Actual Size" in df.columns:
            asize = row.get("Actual Size")
            if pd.notna(asize):
                actual_size = float(asize)

        feature = Feature(
            name=str(row["Feature Name"]),
            feature_type=str(row["Feature Type"]),
            nominal=float(row["Nominal"]),
            tolerance=tolerance,
            measurement=measurement,
            material_condition=material_condition,
            mmc_lmc_size=mmc_lmc_size,
            actual_size=actual_size,
        )

        features.append(feature)

    return Report(source_file=filepath, features=features)