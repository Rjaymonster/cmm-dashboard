from models import Feature

class EvaluationResult:
    """
    Holds the outcome of evaluating a single feature.
    Now includes MMC/LMC bonus tolerance information.
    """

    def __init__(self, feature_name, feature_type, deviation,
                 upper_tolerance, lower_tolerance, is_pass, percent_used,
                 material_condition="RFS", bonus_tolerance=0.0,
                 effective_upper=None, effective_lower=None):
        self.feature_name       = feature_name
        self.feature_type       = feature_type
        self.deviation          = deviation
        self.upper_tolerance    = upper_tolerance
        self.lower_tolerance    = lower_tolerance
        self.is_pass            = is_pass
        self.percent_used       = percent_used
        self.material_condition = material_condition
        self.bonus_tolerance    = bonus_tolerance
        self.effective_upper    = effective_upper if effective_upper is not None else upper_tolerance
        self.effective_lower    = effective_lower if effective_lower is not None else lower_tolerance

    @property
    def has_bonus(self) -> bool:
        """Returns True if bonus tolerance was applied."""
        return self.bonus_tolerance > 0.0

    @property
    def status(self) -> str:
        return "PASS" if self.is_pass else "FAIL"

    @property
    def severity(self) -> str:
        if hasattr(self, '_severity_override'):
            return self._severity_override
        if not self.is_pass:
            return "FAIL"
        if self.percent_used >= 75:
            return "WARNING"
        return "OK"

    def __str__(self):
        bonus_str = f" | bonus: +{self.bonus_tolerance:.4f}" if self.has_bonus else ""
        return (f"{self.feature_name:<10} {self.feature_type:<15} "
                f"{self.status:<6} | dev: {self.deviation:+.4f} | "
                f"tol used: {self.percent_used:.1f}%{bonus_str} | {self.severity}")
    
class BaseEvaluator:
    """
    Base class for all feature type evaluators.
    Contains the core evaluation logic that all feature types share.
    """

    def evaluate(self, feature: Feature,
                 warning_threshold: float = 75.0) -> EvaluationResult:
        """Evaluates a feature and returns an EvaluationResult."""
        is_pass      = feature.is_pass
        percent_used = self._percent_used(feature)

        if not is_pass:
            severity = "FAIL"
        elif percent_used >= warning_threshold:
            severity = "WARNING"
        else:
            severity = "OK"

        result = EvaluationResult(
            feature_name=feature.name,
            feature_type=feature.feature_type,
            deviation=feature.measurement.deviation,
            upper_tolerance=feature.tolerance.upper,
            lower_tolerance=feature.tolerance.lower,
            is_pass=is_pass,
            percent_used=percent_used,
            material_condition=feature.material_condition,
            bonus_tolerance=feature.bonus_tolerance,
            effective_upper=feature.effective_tolerance_upper,
            effective_lower=feature.effective_tolerance_lower,
        )

        # Override severity with threshold-aware value
        result._severity_override = severity
        return result
    
    def _percent_used(self, feature: Feature) -> float:
        """
        Calculates percentage of effective tolerance band consumed.
        Uses effective tolerance so bonus is factored in.
        """
        deviation = feature.measurement.deviation
        if deviation >= 0:
            band = feature.effective_tolerance_upper
        else:
            band = abs(feature.effective_tolerance_lower)

        if band == 0:
            return 100.0

        return (abs(deviation) / band) * 100
    
class CircularityEvaluator(BaseEvaluator):
    """
    Circularity is a form tolerance - always positive.
    A negative Deviation is physically meaningless, treat it as zero.
    """

    def evaluate(self, feature: Feature, warning_threshold: float = 75.0) -> EvaluationResult:
        feature.measurement.deviation = max(0.0, feature.measurement.deviation)
        return super().evaluate(feature, warning_threshold)
    
class FlatnessEvaluator(BaseEvaluator):
    """
    Flastness is a form tolerance - always positive. Same rules a Circularity.
    """

    def evaluate(self, feature: Feature, warning_threshold: float = 75.0) ->EvaluationResult:
        feature.measurement.deviation = max(0.0, feature.measurement.deviation)
        return super().evaluate(feature, warning_threshold)
    
class PositionEvaluator(BaseEvaluator):
    """
    Position is a distance from true position - always positive.
    """

    def evaluate(self, feature: Feature, warning_threshold: float = 75.0) -> EvaluationResult:
        feature.measurement.deviation = abs(feature.measurement.deviation)
        return super().evaluate(feature, warning_threshold)
    
class DiameterEvaluator(BaseEvaluator):
    """
    Diameter is a size tolerance - Can be positive or negative
    Standard +/- band evaluation applies
    """
    pass

class AngularityEvaluator(BaseEvaluator):
    """
    Angularity is an orientation tolerance — always positive.
    """
    def evaluate(self, feature: Feature, warning_threshold: float = 75.0) -> EvaluationResult:
        feature.measurement.deviation = abs(feature.measurement.deviation)
        return super().evaluate(feature, warning_threshold)

class DefaultEvaluator(BaseEvaluator):
    """
    Fallback for any feature type not explicity handled.
    """
    pass

class CylindricityEvaluator(BaseEvaluator):
    """
    Cylindricity is a form tolerance — always positive.
    """
    def evaluate(self, feature: Feature, warning_threshold: float = 75.0) -> EvaluationResult:
        feature.measurement.deviation = max(0.0, feature.measurement.deviation)
        return super().evaluate(feature, warning_threshold)


class StraightnessEvaluator(BaseEvaluator):
    """
    Straightness is a form tolerance — always positive.
    """
    def evaluate(self, feature: Feature, warning_threshold: float = 75.0) -> EvaluationResult:
        feature.measurement.deviation = max(0.0, feature.measurement.deviation)
        return super().evaluate(feature, warning_threshold)


class PerpendicularityEvaluator(BaseEvaluator):
    """
    Perpendicularity is an orientation tolerance — always positive.
    """
    def evaluate(self, feature: Feature, warning_threshold: float = 75.0) -> EvaluationResult:
        feature.measurement.deviation = abs(feature.measurement.deviation)
        return super().evaluate(feature, warning_threshold)


class ParallelismEvaluator(BaseEvaluator):
    """
    Parallelism is an orientation tolerance — always positive.
    """
    def evaluate(self, feature: Feature, warning_threshold: float = 75.0) -> EvaluationResult:
        feature.measurement.deviation = abs(feature.measurement.deviation)
        return super().evaluate(feature, warning_threshold)


class RunoutEvaluator(BaseEvaluator):
    """
    Runout is always positive — it is a measured total indicator reading.
    """
    def evaluate(self, feature: Feature, warning_threshold: float = 75.0) -> EvaluationResult:
        feature.measurement.deviation = abs(feature.measurement.deviation)
        return super().evaluate(feature, warning_threshold)


class TotalRunoutEvaluator(BaseEvaluator):
    """
    Total Runout is always positive — same rules as Runout.
    """
    def evaluate(self, feature: Feature, warning_threshold: float = 75.0) -> EvaluationResult:
        feature.measurement.deviation = abs(feature.measurement.deviation)
        return super().evaluate(feature, warning_threshold)


class ConcentricityEvaluator(BaseEvaluator):
    """
    Concentricity is always positive — it is a derived median point tolerance.
    """
    def evaluate(self, feature: Feature, warning_threshold: float = 75.0) -> EvaluationResult:
        feature.measurement.deviation = abs(feature.measurement.deviation)
        return super().evaluate(feature, warning_threshold)


class ProfileOfLineEvaluator(BaseEvaluator):
    """
    Profile of a Line — bilateral tolerance, standard +/- band evaluation.
    """
    pass


class ProfileOfSurfaceEvaluator(BaseEvaluator):
    """
    Profile of a Surface — bilateral tolerance, standard +/- band evaluation.
    """
    pass


EVALUATOR_MAP = {
    "circularity":        CircularityEvaluator,
    "flatness":           FlatnessEvaluator,
    "position":           PositionEvaluator,
    "diameter":           DiameterEvaluator,
    "angularity":         AngularityEvaluator,
    "cylindricity":       CylindricityEvaluator,
    "straightness":       StraightnessEvaluator,
    "perpendicularity":   PerpendicularityEvaluator,
    "parallelism":        ParallelismEvaluator,
    "runout":             RunoutEvaluator,
    "total runout":       TotalRunoutEvaluator,
    "concentricity":      ConcentricityEvaluator,
    "profile of a line":  ProfileOfLineEvaluator,
    "profile of a surface": ProfileOfSurfaceEvaluator,
}

def get_evaluator(feature_type: str) -> BaseEvaluator:
    """
    Returns the right evaluator for a given feature type.
    Falls back to defaultEvaluator for unknown type.
    """

    key = feature_type.strip().lower()
    evaluator_class = EVALUATOR_MAP.get(key, DefaultEvaluator)
    return evaluator_class()

def evaluate_report(report, warning_threshold: float = 75.0) -> list:
    """
    Evaluates all features in a report.
    Returns a list of EvaluationResult objects.
    warning_threshold controls when a passing feature gets flagged.
    """
    results = []
    for feature in report.features:
        evaluator = get_evaluator(feature.feature_type)
        result = evaluator.evaluate(feature, warning_threshold)
        results.append(result)
    return results