from parser import load_report
from evaluator import evaluate_report, EvaluationResult


class RunData:
    """
    Represents a single inspection run.
    Holds the filename and its evaluation results.
    """

    def __init__(self, filename: str, results: list):
        self.filename = filename
        self.results  = results

    @property
    def run_name(self) -> str:
        """Returns just the filename without the path or tmp_ prefix."""
        name = self.filename.split("/")[-1].split("\\")[-1]
        if name.startswith("tmp_"):
            name = name[4:]
        return name

    @property
    def pass_rate(self) -> float:
        total = len(self.results)
        if total == 0:
            return 0.0
        passes = sum(1 for r in self.results if r.is_pass)
        return (passes / total) * 100


def load_runs(filepaths: list) -> list:
    """
    Loads and evaluates multiple CSV files.
    Returns a list of RunData objects in the order provided.
    """
    filepaths = sorted(filepaths)
    runs = []
    for filepath in filepaths:
        report  = load_report(filepath)
        results = evaluate_report(report)
        runs.append(RunData(filename=filepath, results=results))
    return runs


def get_feature_trend(runs: list, feature_name: str) -> list:
    """
    Extracts the deviation for a specific feature across all runs.
    Returns a list of deviation values in run order.
    """
    trend = []
    for run in runs:
        for result in run.results:
            if result.feature_name == feature_name:
                trend.append(result.deviation)
                break
    return trend


def get_all_feature_names(runs: list) -> list:
    """Returns a list of unique feature names from the first run."""
    if not runs:
        return []
    return [r.feature_name for r in runs[0].results]


def get_feature_stability(runs: list) -> list:
    """
    Ranks features by how much their deviation varies across runs.
    Higher variance = less stable = more concerning.
    Returns a list of (feature_name, variance) tuples sorted by variance.
    """
    feature_names = get_all_feature_names(runs)
    stability = []

    for name in feature_names:
        trend = get_feature_trend(runs, name)
        if len(trend) < 2:
            continue
        mean     = sum(trend) / len(trend)
        variance = sum((x - mean) ** 2 for x in trend) / len(trend)
        stability.append((name, round(variance, 8)))

    return sorted(stability, key=lambda x: x[1], reverse=True)


def is_trending(runs: list, feature_name: str) -> bool:
    trend = get_feature_trend(runs, feature_name)
    if len(trend) < 3:
        return False
    # Count how many consecutive increases there are
    increases = sum(1 for i in range(len(trend) - 1) if trend[i] < trend[i + 1])
    # Flag as trending if more than 60% of steps are increasing
    return increases / (len(trend) - 1) >= 0.6