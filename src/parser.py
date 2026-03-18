import pandas as pd
from models import Tolerance, Measurement, Feature, Report

def load_report(filepath: str) -> Report:
    """
    Reads a MODUS CSV file and returns a Report object.
    Supports optional MMC/LMC columns.
    """
    df = pd.read_csv(filepath)
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

        # Read MMC/LMC columns if they exist
        # The .get() method returns None if the column isn't in the CSV
        # so older files without these columns still work fine
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
