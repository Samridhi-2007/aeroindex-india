import math
import pytest

from intelligence.models import Observation, Weights, WeightMetadata
from intelligence.index_engine.apix import (
    calculate_apix_report,
    select_latest_snapshots,
    calculate_components,
)
from intelligence.data import load_weights, load_cpi_airfare_weight


def test_five_route_basket_aggregation_and_contribution_reconciliation():
    """Verify 5-route basket calculation, route weight sum = 1.0, and contribution reconciliation."""
    weights = load_weights("data/official_route_weights.csv")
    assert len(weights.route_weights) == 5
    assert math.isclose(sum(weights.route_weights.values()), 1.0, abs_tol=1e-9)

    routes = ["DEL-BOM", "DEL-BLR", "BOM-BLR", "DEL-CCU", "DEL-HYD"]
    base_obs = [
        Observation(f"base-{r}", "base", r, r.split("-")[0], r.split("-")[1], 15, 5000.0 + idx * 100, "easemytrip", "IndiGo", "ECONOMY", "2026-09-15", False, "5000", "2026-08-28T08:00:00Z", "extracted", 0, "url")
        for idx, r in enumerate(routes)
    ]
    current_obs = [
        Observation(f"curr-{r}", "current", r, r.split("-")[0], r.split("-")[1], 15, 5500.0 + idx * 110, "easemytrip", "IndiGo", "ECONOMY", "2026-09-20", False, "5500", "2026-08-28T10:00:00Z", "extracted", 0, "url")
        for idx, r in enumerate(routes)
    ]

    report = calculate_apix_report(base_obs + current_obs, weights)

    assert report["calculation_status"] == "OK"
    assert report["weighting_status"] == "OFFICIAL-DATA-DERIVED"
    assert len(report["route_components"]) == 5

    # Check contribution reconciliation: sum(contributions) == APIx
    sum_contributions = sum(r["contribution"] for r in report["route_components"])
    assert math.isclose(sum_contributions, report["apix"], abs_tol=1e-5)


def test_missing_route_in_data_blocks_calculation():
    """Verify that if a route configured in weights has no base/current data, calculation raises ValueError / blocks."""
    weights = load_weights("data/official_route_weights.csv")
    # Missing DEL-HYD
    obs = [
        Observation("b1", "base", "DEL-BOM", "DEL", "BOM", 15, 5000.0, "src", "IndiGo", "ECONOMY", "2026-09-15", False, "5000", "2026-08-28T08:00:00Z", "extracted", 0, "url"),
        Observation("c1", "current", "DEL-BOM", "DEL", "BOM", 15, 5500.0, "src", "IndiGo", "ECONOMY", "2026-09-20", False, "5500", "2026-08-28T10:00:00Z", "extracted", 0, "url"),
    ]

    with pytest.raises(ValueError, match="Configured routes missing from data"):
        calculate_apix_report(obs, weights)


def test_cpi_macro_weight_remains_isolated():
    """Verify that CPI airfare item weight is stored separately and never included in route weights."""
    cpi = load_cpi_airfare_weight("data/cpi_weights.csv", sector="Rural")

    weights = load_weights("data/official_route_weights.csv")

    combined = Weights(
        route_weights=weights.route_weights,
        window_weights=weights.window_weights,
        airfare_weight=cpi.airfare_weight,
        route_weight_metadata=weights.route_weight_metadata,
        window_weight_metadata=weights.window_weight_metadata,
        airfare_weight_metadata=cpi.airfare_weight_metadata,
    )

    assert combined.airfare_weight == 0.01166625043306
    assert "airfare_weight" not in combined.route_weights
    assert math.isclose(sum(combined.route_weights.values()), 1.0, abs_tol=1e-9)
