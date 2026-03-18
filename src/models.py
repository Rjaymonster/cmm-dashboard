class Tolerance:
    """
    Represents the tolerance band for a feature
    upper = the positive limit
    lower = the negative limit
    """
    def __init__(self,upper:float,lower:float):
        self.upper = upper
        self.lower = lower

    def is_in_spec(self, deviation: float) -> bool:
        """Return True if the deviation is within the tolerance band."""
        return self.lower <= deviation <= self.upper
    
class Measurement:
    """
    Represents a single measure result
    actual = the raw measured value
    deviation = how far it is from nominal
    """
    def __init__(self, actual: float, deviation: float):
        self.actual = actual
        self.deviation = deviation

class Feature:
    """
    Represents a single inspected feature.
    Combines identity, tolerance, and measurement into one object.
    Now supports MMC/LMC bonus tolerance.
    """

    def __init__(self, name: str, feature_type: str, nominal: float,
                 tolerance: Tolerance, measurement: Measurement,
                 material_condition: str = "RFS",
                 mmc_lmc_size: float = None,
                 actual_size: float = None):
        self.name = name
        self.feature_type = feature_type
        self.nominal = nominal
        self.tolerance = tolerance
        self.measurement = measurement
        self.material_condition = material_condition.upper().strip() if material_condition else "RFS"
        self.mmc_lmc_size  = mmc_lmc_size
        self.actual_size   = actual_size

    @property
    def bonus_tolerance(self) -> float:
        """
        Calculates bonus tolerance based on material condition.
        Returns 0.0 if RFS or if size data is missing.
        """
        if self.material_condition == "RFS":
            return 0.0
        if self.mmc_lmc_size is None or self.actual_size is None:
            return 0.0
        return abs(self.actual_size - self.mmc_lmc_size)

    @property
    def effective_tolerance_upper(self) -> float:
        """Stated upper tolerance plus any bonus earned."""
        return self.tolerance.upper + self.bonus_tolerance

    @property
    def effective_tolerance_lower(self) -> float:
        """Stated lower tolerance minus any bonus earned."""
        return self.tolerance.lower - self.bonus_tolerance

    @property
    def is_pass(self) -> bool:
        """
        Evaluates pass/fail using effective tolerance —
        which includes any bonus from MMC/LMC.
        """
        return (self.effective_tolerance_lower
                <= self.measurement.deviation
                <= self.effective_tolerance_upper)

    @property
    def status(self) -> str:
        return "PASS" if self.is_pass else "FAIL"
    
class Report:
    """
    Represents a full CMM inspection report.
    Contains a list of Features and can summarize the results.
    """
    def __init__(self, source_file: str, features: list):
        self.source_file = source_file
        self.features = features
    
    @property
    def total(self) ->int:
        return len(self.features)
    
    @property
    def passed(self) -> list:
        return [f for f in self. features if f.is_pass]
    
    @property
    def failed(self) -> list:
        return [f for f in self.features if not f.is_pass]
    
    @property
    def pass_rate(self) -> float:
        if self.total == 0:
            return 0.0
        return (len(self.passed) / self.total) * 100
    
    def summary (self) -> str:
        return (
            f"Report: {self.source_file}\n"
            f" Total: {self.total}\n"
            f" Passed: {len(self.passed)}\n"
            f" Failed: {len(self.failed)}\n"
            f" Pass Rate: {self.pass_rate:.1f}%"
        )