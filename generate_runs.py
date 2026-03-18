# generate_runs.py
# Generates 30 sample run CSV files for capability testing.
# Run once with: python generate_runs.py

import random
import os

# Set a seed so results are reproducible
random.seed(42)

# Feature definitions — name, type, nominal, upper, lower, target deviation, std dev
features = [
    ("CIR1",  "Circularity",       0.0,  0.05,  -0.05,  0.025, 0.008),
    ("CYL1",  "Cylindricity",      0.0,  0.04,  -0.04,  0.018, 0.007),
    ("FLAT1", "Flatness",          0.0,  0.03,  -0.03,  0.012, 0.005),
    ("STR1",  "Straightness",      0.0,  0.025, -0.025, 0.010, 0.004),
    ("POS1",  "Position",          0.0,  0.1,   -0.1,   0.045, 0.015),
    ("CON1",  "Concentricity",     0.0,  0.06,  -0.06,  0.028, 0.009),
    ("DIA1",  "Diameter",         25.0,  0.05,  -0.05,  0.018, 0.008),
    ("ANG1",  "Angularity",        0.0,  0.05,  -0.05,  0.022, 0.007),
    ("PERP1", "Perpendicularity",  0.0,  0.04,  -0.04,  0.019, 0.006),
    ("PAR1",  "Parallelism",       0.0,  0.03,  -0.03,  0.013, 0.005),
    ("RUN1",  "Runout",            0.0,  0.05,  -0.05,  0.021, 0.007),
    ("TRUN1", "Total Runout",      0.0,  0.06,  -0.06,  0.029, 0.009),
    ("POL1",  "Profile of a Line", 0.0,  0.08,  -0.08,  0.038, 0.012),
    ("POS2",  "Profile of a Surface", 0.0, 0.1, -0.1,   0.051, 0.016),
]

# Create output folder
os.makedirs("data/cap_runs", exist_ok=True)

header = ("Feature Name,Feature Type,Nominal,Upper Tolerance,"
          "Lower Tolerance,Actual,Deviation\n")

for run_num in range(1, 31):
    filename = f"data/cap_runs/cap_run{run_num:02d}.csv"
    rows     = [header]

    for name, ftype, nominal, upper, lower, target, std in features:
        # Generate a random deviation centered around target
        deviation = random.gauss(target, std)

        # Keep form tolerances positive
        if ftype in ("Circularity", "Cylindricity", "Flatness",
                     "Straightness", "Runout", "Total Runout"):
            deviation = abs(deviation)

        actual = round(nominal + deviation, 6)
        deviation = round(deviation, 6)

        rows.append(
            f"{name},{ftype},{nominal},{upper},{lower},{actual},{deviation}\n"
        )

    with open(filename, "w") as f:
        f.writelines(rows)

    print(f"Created {filename}")

print(f"\nDone — 30 run files created in cap_runs/")