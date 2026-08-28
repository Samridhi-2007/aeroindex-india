from typing import Any


def route_contributions(components: list[dict[str, Any]], route_weights: dict[str, float]) -> list[dict[str, Any]]:
    totals = dict.fromkeys(route_weights, 0.0)
    for item in components:
        totals[item["route"]] = totals.get(item["route"], 0.0) + item["weighted_contribution"]
    total = sum(totals.values())
    return [{"route": route, "route_weight": route_weights[route], "contribution": value, "base_contribution": route_weights[route] * 100.0, "contribution_change": value - route_weights[route] * 100.0, "contribution_percentage": value / total * 100 if total else 0.0} for route, value in sorted(totals.items(), key=lambda pair: (-pair[1], pair[0]))]


def booking_window_contributions(components: list[dict[str, Any]], window_weights: dict[int, float]) -> list[dict[str, Any]]:
    totals = dict.fromkeys(window_weights, 0.0)
    for item in components:
        totals[item["booking_window_days"]] = totals.get(item["booking_window_days"], 0.0) + item["weighted_contribution"]
    total = sum(totals.values())
    return [{"booking_window_days": window, "window_weight": window_weights[window], "contribution": value, "base_contribution": window_weights[window] * 100.0, "contribution_change": value - window_weights[window] * 100.0, "contribution_percentage": value / total * 100 if total else 0.0} for window, value in sorted(totals.items())]