# modus_parser.py
# Parses MODUS fixed-format text/CSV reports into Report objects.
# Handles the multi-line inspection report format including:
# - One-sided tolerances (form/runout callouts)
# - Datum references in tolerance fields (DAT(A))
# - + prefix on positive tolerances
# - Coordinate data blocks (Curve, Line-Profile point lists)
# - Datum reference annotation lines
# - Part name and date header rows

import re
from models import Feature, Measurement, Tolerance, Report


# --- Feature Type Mapping ---
FEATURE_TYPE_MAP = {
    "circle":    "Circularity",
    "plane":     "Flatness",
    "cylinder":  "Cylindricity",
    "point":     "Point-Profile",
    "line":      "Length",
    "cone":      "Angularity",
    "sphere":    "Circularity",
    "curve":     "Profile of a Surface",
}

# Maps measurement row names to GD&T feature types
MEASUREMENT_TYPE_MAP = {
    "trueposition2d":   "Position",
    "trueposition3d":   "Position",
    "cylindricity":     "Cylindricity",
    "circularity":      "Circularity",
    "flatness":         "Flatness",
    "straightness":     "Straightness",
    "runout":           "Runout",
    "circ.runout":      "Runout",
    "circrunout":       "Runout",
    "totalrunout":      "Total Runout",
    "point-profile":    "Profile of a Surface",
    "surf-profile":     "Profile of a Surface",
    "line-profile":     "Profile of a Line",
    "length_xavg":      "Length",
    "length_yavg":      "Length",
    "length_zavg":      "Length",
    "x-axis":           "Length",
    "y-axis":           "Length",
    "z-axis":           "Length",
    "angle":            "Angularity",
    "angularity":       "Angularity",
    "parallelism":      "Parallelism",
    "perpendicularity": "Perpendicularity",
    "concentricity":    "Concentricity",
    "diameter":         "Diameter",
    "radius":           "Length",
}

# Lines that signal the end of measurement data
SUMMARY_TRIGGERS = [
    "in tolerance count",
    "out tolerance count",
    "total tolerance count",
    "end of report",
    "duration",
]


def _should_skip(line: str) -> bool:
    """Returns True if this line should be skipped entirely."""
    clean = line.strip().lower()

    # Blank or whitespace-only lines
    if not clean:
        return True

    # Separator lines (--- or ===)
    if re.match(r"^[-=]{3,}", clean):
        return True

    # Column header row
    if clean.startswith("(in),"):
        return True

    # Coordinate header rows (Nom.X, Nom.Y etc.)
    if re.match(r"^\s*nom\.x", clean):
        return True

    # Datum reference annotation lines
    if clean.startswith(",") and "datum" in clean:
        return True

    # Page header lines with dates
    if re.search(r"\d{2}-\w{3}-\d{4}", clean):
        return True

    # Coordinate data rows — 6+ numeric fields
    fields = clean.split(",")
    numeric = sum(1 for f in fields[:7] if _is_numeric(f.strip()))
    if numeric >= 6:
        return True

    return False


def _is_summary_row(line: str) -> bool:
    """Returns True if we've hit the summary block at the bottom."""
    clean = line.strip().lower()
    return any(clean.startswith(t) for t in SUMMARY_TRIGGERS)


def _is_numeric(s: str) -> bool:
    """Returns True if string is a valid number (handles + prefix)."""
    try:
        float(s.strip().lstrip("+"))
        return True
    except (ValueError, AttributeError):
        return False


def _clean_numeric(s: str) -> float:
    """Converts string to float, handling + prefix."""
    return float(s.strip().lstrip("+"))


def _is_data_row(fields: list) -> bool:
    """
    Returns True if this is a measurement data row.
    Must have a non-empty first field and a numeric second field.
    """
    if len(fields) < 2:
        return False
    if not fields[0].strip():
        return False
    return _is_numeric(fields[1].strip())


def _parse_tolerances(lo_str: str, hi_str: str, nominal: float):
    """
    Parses tolerance fields which may contain:
    - Normal values: -0.0039, +0.0039
    - Datum references: DAT(A)
    - Empty fields (one-sided tolerances)

    For one-sided tolerances where nominal IS the tolerance limit
    (e.g. Circularity,0.0000,0.0039,,,,*---) returns [0.0, nominal].
    """
    lo_str = lo_str.strip()
    hi_str = hi_str.strip()

    lo_is_datum = not lo_str or lo_str.upper().startswith("DAT")
    hi_is_datum = not hi_str or hi_str.upper().startswith("DAT")

    if lo_is_datum and hi_is_datum:
        # One-sided tolerance — nominal holds the upper limit
        if nominal > 0:
            return 0.0, nominal
        else:
            return -0.001, 0.001

    try:
        lower = _clean_numeric(lo_str) if not lo_is_datum else 0.0
    except ValueError:
        lower = 0.0

    try:
        upper = _clean_numeric(hi_str) if not hi_is_datum else 0.001
    except ValueError:
        upper = 0.001

    return lower, upper


def _parse_feature_header(line: str):
    """
    Parses a feature header line like 'Circle:CIR001' or
    'Cylinder:CYL001--Line:LINE001'.
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
    Handles real MODUS format including + prefixes and datum references.
    """
    try:
        meas_name = fields[0].strip()

        actual  = _clean_numeric(fields[1]) if len(fields) > 1 and fields[1].strip() else 0.0

        # Nominal field may be empty or contain a datum reference
        nominal_str = fields[2].strip() if len(fields) > 2 else ""
        if nominal_str and not nominal_str.upper().startswith("DAT") and _is_numeric(nominal_str):
            nominal = _clean_numeric(nominal_str)
        else:
            nominal = 0.0

        lo_str = fields[3].strip() if len(fields) > 3 else ""
        hi_str = fields[4].strip() if len(fields) > 4 else ""

        lower, upper = _parse_tolerances(lo_str, hi_str, nominal)

        # If nominal was used as tolerance, reset it to 0
        if lower == 0.0 and upper == nominal and nominal > 0:
            nominal = 0.0

        # Deviation field
        dev_str = fields[5].strip() if len(fields) > 5 else ""
        if dev_str and _is_numeric(dev_str):
            deviation = _clean_numeric(dev_str)
        else:
            deviation = actual - nominal

        # Map measurement name to GD&T type
        meas_key  = meas_name.lower().replace(" ", "").replace(".", "")
        feat_type = MEASUREMENT_TYPE_MAP.get(meas_key, feature_type)
        full_name = f"{feature_name}_{meas_name}"

        tolerance   = Tolerance(upper=upper, lower=lower)
        measurement = Measurement(actual=actual, deviation=deviation)

        return Feature(
            name=full_name,
            feature_type=feat_type,
            nominal=nominal,
            tolerance=tolerance,
            measurement=measurement,
        )

    except Exception:
        return None


def load_modus_report(filepath: str) -> Report:
    """
    Parses a MODUS fixed-format report file into a Report object.
    Handles .csv, .txt, .res, and .rtf versions of the format.
    """
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    features     = []
    current_name = "UNKNOWN"
    current_type = "Length"

    for line in lines:
        # Stop at summary block
        if _is_summary_row(line):
            break

        # Skip non-data lines
        if _should_skip(line):
            continue

        clean  = line.strip()
        fields = clean.split(",")

        # Feature header line e.g. Circle:CIR001
        if ":" in fields[0] and not _is_data_row(fields):
            current_name, current_type = _parse_feature_header(fields[0])
            continue

        # Data row
        if _is_data_row(fields):
            feature = _parse_data_row(fields, current_name, current_type)
            if feature:
                features.append(feature)

    return Report(source_file=filepath, features=features)
