import math
from typing import Any

from ..models import Observation, Weights
from .weighting import validate_weights


def price_relative(base_fare: float | None, current_fare: float | None) -> float:
    """Calculate 100 times current representative fare divided by base fare."""
    if base_fare is None or current_fare is None or base_fare <= 0 or current_fare <= 0:
        return 0.0
    return 100.0 * current_fare / base_fare


def jevons_index(relatives: list[tuple[float, float]]) -> float:
    """Calculate a weighted Jevons index from (weight, price relative) pairs."""
    valid = [(weight, relative) for weight, relative in relatives if weight > 0 and relative > 0 and math.isfinite(relative)]
    if not valid:
        return 0.0
    weight_total = sum(weight for weight, _ in valid)
    return math.exp(sum(weight * math.log(relative) for weight, relative in valid) / weight_total)


def elementary_index(price_pairs: list[tuple[float, float]]) -> float:
    """Calculate the unweighted Jevons elementary index from comparable prices."""
    relatives = [(1.0, 100.0 * current / base) for base, current in price_pairs if base > 0 and current > 0 and math.isfinite(base) and math.isfinite(current)]
    return jevons_index(relatives)


def select_latest_snapshots(observations: list[Observation], base_period: str = "base", current_period: str = "current") -> list[Observation]:
    """Filter observations to the latest collection timestamp for base and current periods per route."""
    routes = {o.route for o in observations}
    filtered = []
    for route in routes:
        route_base_obs = [o for o in observations if o.route == route and o.period == base_period]
        route_current_obs = [o for o in observations if o.route == route and o.period == current_period]

        base_ts = max((o.collection_timestamp for o in route_base_obs if o.collection_timestamp), default=None)
        current_ts = max((o.collection_timestamp for o in route_current_obs if o.collection_timestamp), default=None)

        if base_ts:
            filtered.extend([o for o in route_base_obs if o.collection_timestamp == base_ts])
        else:
            filtered.extend(route_base_obs)

        if current_ts:
            filtered.extend([o for o in route_current_obs if o.collection_timestamp == current_ts])
        else:
            filtered.extend(route_current_obs)

    return filtered



def calculate_components(observations: list[Observation], weights: Weights, base_period: str = "base", current_period: str = "current") -> list[dict[str, Any]]:
    observations = select_latest_snapshots(observations, base_period, current_period)
    groups: dict[tuple[str, int, str, str], dict[str, list[float]]] = {}
    for item in observations:
        if item.total_consumer_fare is None or item.total_consumer_fare <= 0 or not math.isfinite(item.total_consumer_fare):
            continue
        key = (item.route, item.booking_window_days, item.carrier, item.fare_class)
        groups.setdefault(key, {base_period: [], current_period: []}).setdefault(item.period, []).append(item.total_consumer_fare)
    result = []
    target_routes = sorted(weights.route_weights.keys()) if weights.route_weights else sorted({item.route for item in observations})
    for route in target_routes:
        route_weight = weights.route_weights.get(route, 0.0)
        route_pairs = []
        for (group_route, window, carrier, fare_class), values in sorted(groups.items(), key=lambda entry: tuple(str(value) for value in entry[0])):
            if group_route != route:
                continue
            base_values = sorted(values.get(base_period, []))
            current_values = sorted(values.get(current_period, []))
            route_pairs.extend(zip(base_values, current_values))
            if base_values and current_values:
                base = base_values[len(base_values) // 2]
                current = current_values[len(current_values) // 2]
                result.append({"route": route, "booking_window_days": window, "carrier": carrier, "fare_class": fare_class, "route_weight": route_weight, "base_representative_fare": base, "current_representative_fare": current, "elementary_index": elementary_index(list(zip(base_values, current_values))), "comparable_observations": min(len(base_values), len(current_values))})
        route_index = elementary_index(route_pairs)
        for item in result:
            if item["route"] == route:
                item["route_elementary_index"] = route_index
    return result



def matching_validation_issues(observations: list[Observation], weights: Weights, base_period: str = "base", current_period: str = "current") -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    base_obs = [item for item in observations if item.period == base_period and item.total_consumer_fare and item.total_consumer_fare > 0]
    current_obs = [item for item in observations if item.period == current_period and item.total_consumer_fare and item.total_consumer_fare > 0]

    if not base_obs:
        issues.append({"issue_type": "missing_genuine_base_period", "detail": f"No genuine historical {base_period} period observations found in repository"})
    if not current_obs:
        issues.append({"issue_type": "missing_current_period", "detail": f"No valid {current_period} period observations found in repository"})

    if base_obs and current_obs:
        base_fares = sorted([o.total_consumer_fare for o in base_obs])
        current_fares = sorted([o.total_consumer_fare for o in current_obs])
        base_timestamps = {o.collection_timestamp for o in base_obs if o.collection_timestamp}
        current_timestamps = {o.collection_timestamp for o in current_obs if o.collection_timestamp}
        base_ids = {o.observation_id.replace(f"-{base_period}-", f"-{current_period}-") for o in base_obs}
        current_ids = {o.observation_id for o in current_obs}

        if base_fares == current_fares and (base_timestamps == current_timestamps or base_ids == current_ids):
            issues.append({
                "issue_type": "missing_genuine_base_period",
                "detail": "Base observations are identical duplicates of current observations from the same collection run. A genuine earlier historical base snapshot is required."
            })

    for route in weights.route_weights:
        b_count = sum(1 for item in base_obs if item.route == route)
        c_count = sum(1 for item in current_obs if item.route == route)
        if min(b_count, c_count) < 1 and not any(i["issue_type"] == "missing_genuine_base_period" for i in issues):
            issues.append({"issue_type": "insufficient_comparable_observations", "route": route, "detail": f"At least one valid base/current pair is required for route {route}"})
    return issues


def calculate_apix_report(observations: list[Observation], weights: Weights, base_period: str = "base", current_period: str = "current") -> dict[str, Any]:
    """Run the complete APIx pipeline and return JSON-serializable data."""
    from ..insights.explanations import generate_insights
    from ..quality.confidence import calculate_confidence

    validate_weights(weights, observations)
    matching_issues = matching_validation_issues(observations, weights, base_period, current_period)
    components = calculate_components(observations, weights, base_period, current_period)
    if matching_issues:
        is_missing_base = any(i["issue_type"] in ("missing_base_match", "missing_genuine_base_period") for i in matching_issues)
        reason = "MISSING_GENUINE_BASE_PERIOD" if is_missing_base else "MATCHING_FAILED"
        return {"apix": None, "base": 100.0, "index_name": "Airfare Price Index", "calculation_status": "BLOCKED", "reason": reason, "weighting_status": "OFFICIAL-WEIGHTED" if weights.route_weight_metadata and all(item.status.lower() == "official" for item in weights.route_weight_metadata.values()) else "CONFIGURED-WEIGHTED", "methodology": "CPI 2024 / Jevons elementary indices aggregated with authoritative route weights", "airfare_weight": weights.airfare_weight, "airfare_weight_metadata": weights.airfare_weight_metadata.__dict__ if weights.airfare_weight_metadata else None, "route_components": [], "booking_window_components": [], "components": components, "validation_issues": matching_issues, "confidence": calculate_confidence(observations, weights), "insights": []}
    route_indices = {route: next((item["route_elementary_index"] for item in components if item["route"] == route), 0.0) for route in weights.route_weights}
    apix = sum(weights.route_weights[route] * index for route, index in route_indices.items())
    routes = [{"route": route, "route_weight": weights.route_weights[route], "weight_metadata": weights.route_weight_metadata.get(route).__dict__ if route in weights.route_weight_metadata else None, "elementary_index": index, "base_representative_fare": next((c.get("base_representative_fare") for c in components if c.get("route") == route and c.get("base_representative_fare") is not None), None), "current_representative_fare": next((c.get("current_representative_fare") for c in components if c.get("route") == route and c.get("current_representative_fare") is not None), None), "contribution": weights.route_weights[route] * index, "base_contribution": weights.route_weights[route] * 100.0, "contribution_change": weights.route_weights[route] * (index - 100.0), "contribution_percentage": (weights.route_weights[route] * index / apix * 100) if apix else 0.0} for route, index in sorted(route_indices.items(), key=lambda pair: (-weights.route_weights[pair[0]] * pair[1], pair[0]))]

    windows = [{"booking_window_days": window, "statistical_weight": None, "weight_metadata": None, "contribution": None, "contribution_change": 0.0, "comparable_observations": sum(item["comparable_observations"] for item in components if item["booking_window_days"] == window)} for window in sorted({item.booking_window_days for item in observations})]
    if weights.route_weight_metadata and all(item.status.lower() == "official" for item in weights.route_weight_metadata.values()):
        weighting_status = "OFFICIAL-WEIGHTED"
    elif weights.route_weight_metadata and any("derived" in item.status.lower() for item in weights.route_weight_metadata.values()):
        weighting_status = "OFFICIAL-DATA-DERIVED"
    elif any(item.status.lower() == "demonstration" for item in weights.route_weight_metadata.values()):
        weighting_status = "DEMONSTRATION-WEIGHTED"
    else:
        weighting_status = "CONFIGURED-WEIGHTED"
    index_change = apix - 100.0 if apix is not None else None
    index_change_pct = apix - 100.0 if apix is not None else None
    return {"apix": apix, "base": 100.0, "index_change": index_change, "index_change_percentage": index_change_pct, "index_name": "Airfare Price Index", "calculation_status": "OK", "weighting_status": weighting_status, "methodology": "CPI 2024 / Jevons elementary indices aggregated with authoritative route weights", "airfare_weight": weights.airfare_weight, "airfare_weight_metadata": weights.airfare_weight_metadata.__dict__ if weights.airfare_weight_metadata else None, "route_components": routes, "booking_window_components": windows, "components": components, "validation_issues": [], "confidence": calculate_confidence(observations, weights), "insights": generate_insights(apix, routes, windows)}
