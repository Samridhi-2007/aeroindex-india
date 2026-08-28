from dataclasses import replace

import pytest

from intelligence.data import load_observations, load_weights
from intelligence.index_engine.apix import calculate_apix_report, jevons_index, price_relative
from intelligence.index_engine.contributions import booking_window_contributions, route_contributions
from intelligence.index_engine.weighting import representative_fares, validate_weights
from intelligence.insights.explanations import generate_insights
from intelligence.models import Observation, Weights
from intelligence.quality.confidence import calculate_confidence, calculate_outlier_stability


def obs(route="R", window=1, period="base", fare=100, observation_id="1", duplicate=False):
    return Observation(observation_id, period, route, "A", "B", window, fare, "S", "C", "E", "2026-01-01", duplicate)


def test_median_and_price_relative_and_invalid_base():
    assert representative_fares([obs(fare=4750, observation_id="1"), obs(fare=4800, observation_id="2"), obs(fare=4850, observation_id="3")])[("R", 1, "base")] == 4800
    assert price_relative(100, 120) == 120
    assert price_relative(0, 120) == 0


def test_jevons_index_is_weighted_geometric_mean():
    assert jevons_index([(0.5, 120), (0.5, 100)]) == pytest.approx((120 * 100) ** 0.5)


def test_weights_and_hand_calculated_apix():
    weights = Weights({"R": 0.5, "Q": 0.5}, {1: 1.0})
    items = [obs("R", fare=100), obs("R", period="current", fare=120), obs("Q", fare=100), obs("Q", period="current", fare=100)]
    validate_weights(weights, items, (1,))
    report = calculate_apix_report(items, weights)
    assert report["apix"] == pytest.approx(110)
    assert report["route_components"][0]["contribution"] == pytest.approx(60)
    assert sum(item["contribution"] for item in report["route_components"]) == pytest.approx(report["apix"])


def test_invalid_weights_fail():
    items = [obs()]
    invalid_route_weights = Weights({"R": 0.8}, {1: 1})
    invalid_window_weights = Weights({"R": 1}, {1: 0.5})
    with pytest.raises(ValueError):
        validate_weights(invalid_route_weights, items, (1,))
    validate_weights(invalid_window_weights, items, (1,))


def test_contributions_reconcile_and_windows():
    components = [{"route": "R", "booking_window_days": 1, "weighted_contribution": 60}, {"route": "Q", "booking_window_days": 7, "weighted_contribution": 40}]
    routes = route_contributions(components, {"R": 0.5, "Q": 0.5})
    windows = booking_window_contributions(components, {1: 0.5, 7: 0.5})
    assert sum(item["contribution"] for item in routes) == pytest.approx(100)
    assert windows[0]["contribution"] == 60


def test_confidence_missing_duplicate_outlier_and_determinism():
    weights = Weights({"R": 1}, {1: 1})
    items = [obs(fare=100), obs(period="current", fare=120)]
    clean = calculate_confidence(items, weights)
    assert clean == calculate_confidence(items, weights)
    damaged = [replace(items[0], observation_id="", is_duplicate=True), replace(items[1], total_consumer_fare=10000)]
    assert calculate_confidence(damaged, weights)["overall_confidence"] < clean["overall_confidence"]
    assert calculate_outlier_stability([obs(fare=value, observation_id=str(value)) for value in (100, 101, 102, 10000)]) < 100


def test_report_and_insights_determinism():
    weights = Weights({"R": 1.0}, {1: 1.0})
    items = [obs("R", fare=100, observation_id="1"), obs("R", period="current", fare=105, observation_id="2")]
    report = calculate_apix_report(items, weights)
    assert report == calculate_apix_report(items, weights)
    assert report["base"] == 100
    assert len(report["insights"]) == 3
    assert generate_insights(102, report["route_components"], report["booking_window_components"])[0]["direction"] == "UP"