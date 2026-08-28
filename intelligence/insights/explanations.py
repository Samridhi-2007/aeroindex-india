from typing import Any


def generate_index_movement_insight(apix: float) -> dict[str, Any]:
    change = apix - 100.0
    if change > 0:
        direction = "UP"
    elif change < 0:
        direction = "DOWN"
    else:
        direction = "UNCHANGED"
    return {"type": "INDEX_MOVEMENT", "direction": direction, "change": change}


def generate_route_driver_insight(routes: list[dict[str, Any]]) -> dict[str, Any]:
    return {"type": "ROUTE_DRIVERS", "drivers": routes[:3]}


def generate_booking_window_driver_insight(windows: list[dict[str, Any]]) -> dict[str, Any]:
    driver = max(windows, key=lambda item: item["contribution_change"], default={"booking_window_days": None, "contribution_change": 0.0})
    return {"type": "BOOKING_WINDOW_DRIVER", "window": driver["booking_window_days"], "contribution_change": driver["contribution_change"]}


def generate_insights(apix: float, routes: list[dict[str, Any]], windows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [generate_index_movement_insight(apix), generate_route_driver_insight(routes), generate_booking_window_driver_insight(windows)]