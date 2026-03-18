# modus_parser.py
# Parses MODUS fixed-format text/CSV reports into Report objects.
# Handles the multi-line inspection report format where features
# are grouped under INSPECTION ITEM blocks.

import re
from models import Feature, Measurement, Tolerance, Report


# --- Feature Type Mapping ---
# Maps MODUS feature type prefixes to GD&T feature type names

FEATURE_TYPE_MAP = {
    "circle":    "Circularity",
    "plane":     "Flatness",
    "cylinder":  "Cylindricity",
    "point":     "Point-Profile",
    "line":      "Length",
    "cone":      "Angularity",
    "sphere":    "Circularity",
}

# Maps measurement row names to GD&T feature types
MEASUREMENT_TYPE_MAP = {
    "trueposition2d":  "Position",
    "trueposition3d":  "Position",
    "cylindricity":    "Cylindricity",
    "circularity":     "Circularity",
    "flatness":        "Flatness",
    "straightness":    "Straightness",
    "runout":          "Runout",
    "totalrunout":     "Total Runout",
    "point-profile":   "Profile of a Surface",
    "line-profile":    "Profile of a Line",
    "length_xavg":     "Length",
    "length_yavg":     "Length",
    "length_zavg":     "Length",
    "x-axis":          "Length",
    "y-axis":          "Length",
    "z-axis":          "Length",
}


def _is_data_row(fields: list) -> bool:
    """
    Returns True if this row is a measurement data row.
    A data row has a measurement name in field 0 and
    a number in field 1.
    """
    if len(fields) < 2:
        return False
    try:
        float(fields[1])
        return True
    except ValueError:
        return False


def _is_summary_row(line: str) -> bool:
    """Returns True if we've hit the summary block at the bottom."""
    triggers = [
        "in tolerance count",
        "out tolerance count",
        "total tolerance count",
        "end of report",
        "duration:",
        "pass",
        "fail",
        "in:,",
        "out:,",
    ]
    return any(line.lower().startswith(t) for t in triggers)


def _parse_feature_header(line: str) -> tuple:
    """
    Parses a feature header line like 'Circle:CIR1' or
    'Point:POINT1--Line:LINE1'.
    Returns (feature_name, feature_type).
    """
    primary = line.split("--")[0].strip()

    if ":" in primary:
        type_prefix, name = primary.split(":", 1)
        feature_type = FEATURE_TYPE_MAP.get(
            type_prefix.strip().lower(), "Length"
        )
        feature_name = name.strip()
    else:
        feature_type = "Length"
        feature_name = primary.strip()

    return feature_name, feature_type


def _parse_data_row(fields: list, feature_name: str,
                    feature_type: str) -> Feature | None:
    """
    Parses a measurement data row into a Feature object.
    Fields: measurement_name, actual, nominal, lo_tol, hi_tol, deviation
    """
    try:
        measurement_name = fields[0].strip()

        actual    = float(fields[1]) if fields[1].strip() else 0.0
        nominal   = float(fields[2]) if len(fields) > 2 and fields[2].strip() else 0.0
        lo_tol    = float(fields[3]) if len(fields) > 3 and fields[3].strip() else -0.001
        hi_tol    = float(fields[4]) if len(fields) > 4 and fields[4].strip() else 0.001
        deviation = float(fields[5]) if len(fields) > 5 and fields[5].strip() else 0.0

        meas_key  = measurement_name.lower().replace(" ", "")
        feat_type = MEASUREMENT_TYPE_MAP.get(meas_key, feature_type)
        full_name = f"{feature_name}_{measurement_name}"

        tolerance   = Tolerance(upper=hi_tol, lower=lo_tol)
        measurement = Measurement(actual=actual, deviation=deviation)

        return Feature(
            name=full_name,
            feature_type=feat_type,
            nominal=nominal,
            tolerance=tolerance,
            measurement=measurement,
        )

    except (ValueError, IndexError):
        return None


def load_modus_report(filepath: str) -> Report:
    """
    Parses a MODUS fixed-format report file into a Report object.
    """
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    features     = []
    current_name = "UNKNOWN"
    current_type = "Length"

    for line in lines:
        clean = line.strip()

        if not clean:
            continue
        if _is_summary_row(clean):
            break
        if clean.startswith("PROGRAM") or clean.startswith("DATETIME"):
            continue
        if clean.startswith("(in),"):
            continue
        if clean.startswith("INSPECTION ITEM"):
            continue

        fields = clean.split(",")

        if ":" in fields[0] and not _is_data_row(fields):
            current_name, current_type = _parse_feature_header(fields[0])
            continue

        if _is_data_row(fields):
            feature = _parse_data_row(fields, current_name, current_type)
            if feature:
                features.append(feature)

    return Report(source_file=filepath, features=features)