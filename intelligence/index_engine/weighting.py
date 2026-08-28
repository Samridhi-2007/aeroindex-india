import math
from collections import defaultdict

from ..models import Observation, Weights


def validate_weights(weights: Weights, observations: list[Observation], expected_windows: tuple[int, ...] = (1, 7, 15, 30, 45)) -> None:
    """Validate externally supplied route weights; windows are collection parameters only."""
    if not weights.route_weights or any(value < 0 or not math.isfinite(value) for value in weights.route_weights.values()) or not math.isclose(sum(weights.route_weights.values()), 1.0, abs_tol=1e-9):
        raise ValueError("Authoritative route weights must be finite, non-negative, and sum to 1")
    missing_routes = set(weights.route_weights) - {item.route for item in observations}
    if missing_routes:
        raise ValueError(f"Configured routes missing from data: {sorted(missing_routes)}")


def representative_fares(observations: list[Observation]) -> dict[tuple[str, int, str], float]:
    """Return the median positive fare per route/window/period group."""
    groups: dict[tuple[str, int, str], list[float]] = defaultdict(list)
    for item in observations:
        if item.total_consumer_fare is not None and math.isfinite(item.total_consumer_fare) and item.total_consumer_fare > 0:
            groups[(item.route, item.booking_window_days, item.period)].append(item.total_consumer_fare)
    result = {}
    for key, values in groups.items():
        values.sort()
        midpoint = len(values) // 2
        result[key] = values[midpoint] if len(values) % 2 else (values[midpoint - 1] + values[midpoint]) / 2
    return result