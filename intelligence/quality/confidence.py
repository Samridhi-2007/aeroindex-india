from ..data import REQUIRED_COLUMNS
from ..models import Observation, Weights


def _valid(items: list[Observation]) -> list[Observation]:
    return [item for item in items if item.total_consumer_fare is not None and item.total_consumer_fare > 0]


def calculate_source_coverage(observations: list[Observation], expected_sources: set[str] | None = None) -> float:
    sources = {item.source_id for item in observations if item.source_id}
    expected = expected_sources or sources
    return 100.0 * len(sources & expected) / len(expected) if expected else 0.0


def calculate_route_coverage(observations: list[Observation], configured_routes: set[str]) -> float:
    valid_routes = {item.route for item in _valid(observations)}
    return 100.0 * len(valid_routes & configured_routes) / len(configured_routes) if configured_routes else 0.0


def calculate_booking_window_coverage(observations: list[Observation], configured_routes: set[str], expected_windows: set[int] | None = None) -> float:
    windows = expected_windows or {1, 7, 15, 30, 45}
    observed = {(item.route, item.booking_window_days) for item in _valid(observations)}
    expected = {(route, window) for route in configured_routes for window in windows}
    return 100.0 * len(observed & expected) / len(expected) if expected else 0.0


def calculate_field_completeness(observations: list[Observation]) -> float:
    fields = ("observation_id", "period", "route", "booking_window_days", "total_consumer_fare", "source_id", "observation_date")
    present = sum(getattr(item, field) is not None and getattr(item, field) != "" for item in observations for field in fields)
    return 100.0 * present / (len(observations) * len(fields)) if observations else 0.0


def calculate_duplicate_quality(observations: list[Observation]) -> float:
    if not observations:
        return 0.0
    keys = [(item.observation_id, item.period, item.route, item.booking_window_days, item.total_consumer_fare) for item in observations]
    contamination = len(keys) - len(set(keys)) + sum(item.is_duplicate for item in observations)
    return max(0.0, 100.0 * (1.0 - contamination / len(observations)))


def calculate_outlier_stability(observations: list[Observation]) -> float:
    values = sorted(item.total_consumer_fare for item in _valid(observations))
    if len(values) < 4:
        return 100.0 if values else 0.0
    q1 = values[(len(values) - 1) // 4]
    q3 = values[3 * (len(values) - 1) // 4]
    iqr = q3 - q1
    if iqr == 0:
        return 100.0
    outliers = sum(value < q1 - 1.5 * iqr or value > q3 + 1.5 * iqr for value in values)
    return max(0.0, 100.0 * (1.0 - outliers / len(values)))


def calculate_schema_stability() -> float:
    """Score the fixed typed schema; malformed CSVs are rejected at load time."""
    return 100.0 if set(Observation.__dataclass_fields__) == REQUIRED_COLUMNS else 0.0


def calculate_confidence(observations: list[Observation], weights: Weights, expected_sources: set[str] | None = None) -> dict[str, float]:
    scores = {"source_coverage": calculate_source_coverage(observations, expected_sources), "route_coverage": calculate_route_coverage(observations, set(weights.route_weights)), "booking_window_coverage": calculate_booking_window_coverage(observations, set(weights.route_weights), set(weights.window_weights)), "field_completeness": calculate_field_completeness(observations), "duplicate_quality": calculate_duplicate_quality(observations), "outlier_stability": calculate_outlier_stability(observations), "schema_stability": calculate_schema_stability()}
    scores["overall_confidence"] = 0.25 * scores["source_coverage"] + 0.20 * scores["route_coverage"] + 0.15 * scores["booking_window_coverage"] + 0.15 * scores["field_completeness"] + 0.10 * scores["duplicate_quality"] + 0.10 * scores["outlier_stability"] + 0.05 * scores["schema_stability"]
    scores = {key: max(0.0, min(100.0, value)) for key, value in scores.items()}
    return scores