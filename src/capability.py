# capability.py
# Calculates Cp and Cpk process capability indices.
#
# New concept: statistics
# We use Python's built-in statistics module for mean and stdev.
# No extra libraries needed.

import statistics


class CapabilityResult:
    """
    Holds Cp and Cpk results for a single feature.
    """

    def __init__(self, feature_name: str, feature_type: str,
                 upper_tol: float, lower_tol: float,
                 mean: float, std_dev: float,
                 cp: float, cpk: float, sample_count: int):
        self.feature_name  = feature_name
        self.feature_type  = feature_type
        self.upper_tol     = upper_tol
        self.lower_tol     = lower_tol
        self.mean          = mean
        self.std_dev       = std_dev
        self.cp            = cp
        self.cpk           = cpk
        self.sample_count  = sample_count

    @property
    def rating(self) -> str:
        """
        Industry standard Cpk rating:
        >= 1.67  Excellent
        >= 1.33  Capable
        >= 1.00  Marginal
        <  1.00  Not Capable
        """
        if self.cpk >= 1.67:
            return "Excellent"
        if self.cpk >= 1.33:
            return "Capable"
        if self.cpk >= 1.00:
            return "Marginal"
        return "Not Capable"

    @property
    def color(self) -> str:
        """Returns a color string based on rating."""
        return {
            "Excellent":    "#00C896",
            "Capable":      "#4A90D9",
            "Marginal":     "#FFA500",
            "Not Capable":  "#FF4C4C",
        }.get(self.rating, "#7B8099")

    def __str__(self):
        return (
            f"{self.feature_name:<10} {self.feature_type:<15} "
            f"Cp: {self.cp:.3f}  Cpk: {self.cpk:.3f}  "
            f"n={self.sample_count}  [{self.rating}]"
        )


def calculate_capability(feature_name: str, feature_type: str,
                         deviations: list, upper_tol: float,
                         lower_tol: float) -> CapabilityResult | None:
    """
    Calculates Cp and Cpk for a feature given a list of deviation values.
    Returns None if there are fewer than 2 samples.

    Args:
        feature_name  : name of the feature
        feature_type  : type of the feature
        deviations    : list of deviation values across samples/runs
        upper_tol     : upper tolerance limit
        lower_tol     : lower tolerance limit
    """
    if len(deviations) < 2:
        return None

    mean    = statistics.mean(deviations)
    std_dev = statistics.stdev(deviations)

    if std_dev == 0:
        return None

    tol_range = upper_tol - lower_tol

    # Cp — process spread vs tolerance band
    cp = tol_range / (6 * std_dev)

    # Cpk — centered capability
    cpu = (upper_tol - mean) / (3 * std_dev)
    cpl = (mean - lower_tol) / (3 * std_dev)
    cpk = min(cpu, cpl)

    return CapabilityResult(
        feature_name=feature_name,
        feature_type=feature_type,
        upper_tol=upper_tol,
        lower_tol=lower_tol,
        mean=round(mean, 6),
        std_dev=round(std_dev, 6),
        cp=round(cp, 3),
        cpk=round(cpk, 3),
        sample_count=len(deviations),
    )


def capability_from_runs(runs: list) -> list:
    """
    Calculates Cp and Cpk for each feature across multiple runs.
    Uses deviation values from each run as the sample set.
    """
    from trend import get_all_feature_names, get_feature_trend

    feature_names = get_all_feature_names(runs)
    results       = []

    for name in feature_names:
        deviations = get_feature_trend(runs, name)

        # Get tolerance from first run
        upper_tol = None
        lower_tol = None
        feat_type = ""
        for result in runs[0].results:
            if result.feature_name == name:
                upper_tol = result.upper_tolerance
                lower_tol = result.lower_tolerance
                feat_type = result.feature_type
                break

        if upper_tol is None:
            continue

        cap = calculate_capability(name, feat_type, deviations,
                                   upper_tol, lower_tol)
        if cap:
            results.append(cap)

    return results


def capability_from_report(report) -> list:
    """
    Calculates Cp and Cpk from a single report where each feature
    has multiple sample readings in the CSV.
    Expects a 'Sample' column in the CSV grouping readings by feature.
    """
    from collections import defaultdict

    feature_data: dict = defaultdict(list)
    feature_meta: dict = {}

    for feature in report.features:
        name = feature.name
        feature_data[name].append(feature.measurement.deviation)
        if name not in feature_meta:
            feature_meta[name] = {
                "type":  feature.feature_type,
                "upper": feature.tolerance.upper,
                "lower": feature.tolerance.lower,
            }

    results = []
    for name, deviations in feature_data.items():
        meta = feature_meta[name]
        cap  = calculate_capability(
            name, meta["type"], deviations,
            meta["upper"], meta["lower"]
        )
        if cap:
            results.append(cap)

    return results