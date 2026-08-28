import math
import sqlite3
import pytest
from pathlib import Path

from intelligence.models import Observation, Weights, WeightMetadata
from intelligence.index_engine.apix import (
    calculate_apix_report,
    select_latest_snapshots,
    matching_validation_issues,
)
from intelligence.storage import IntelligenceRepository


def test_two_independently_collected_snapshots_succeeds_with_valid_weights():
    """Verify that two independently collected snapshots with valid route weights produce a valid APIx."""
    base_obs = [
        Observation("easemytrip-base-1", "base", "DEL-BOM", "DEL", "BOM", 15, 6000.0, "easemytrip", "IndiGo", "ECONOMY", "2026-09-15", False, "₹6,000", "2026-08-28T08:00:00Z", "extracted", 0, "url"),
    ]
    current_obs = [
        Observation("easemytrip-current-1", "current", "DEL-BOM", "DEL", "BOM", 15, 6600.0, "easemytrip", "IndiGo", "ECONOMY", "2026-09-20", False, "₹6,600", "2026-08-28T10:00:00Z", "extracted", 0, "url"),
    ]

    weights = Weights(
        route_weights={"DEL-BOM": 1.0},
        window_weights={15: 1.0},
        airfare_weight=0.01166625043306,
        route_weight_metadata={"DEL-BOM": WeightMetadata("official_basket", "official", "CPI 2024 Table 4")},
        window_weight_metadata={15: WeightMetadata("param", "configured", "Window Param")},
        airfare_weight_metadata=WeightMetadata("official_item", "official", "CPI 2024 Airfare Item Weight Reference"),
    )

    report = calculate_apix_report(base_obs + current_obs, weights)

    assert report["calculation_status"] == "OK"
    assert report["weighting_status"] == "OFFICIAL-WEIGHTED"
    assert math.isclose(report["apix"], 110.0, abs_tol=1e-5)


def test_same_collection_timestamp_for_base_and_current_blocked():
    """Verify that using the exact same collection timestamp for BASE and CURRENT is BLOCKED."""
    timestamp = "2026-08-28T08:00:00Z"
    obs = [
        Observation("obs-base-1", "base", "DEL-BOM", "DEL", "BOM", 15, 6000.0, "easemytrip", "IndiGo", "ECONOMY", "2026-09-15", False, "₹6,000", timestamp, "extracted", 0, "url"),
        Observation("obs-current-1", "current", "DEL-BOM", "DEL", "BOM", 15, 6000.0, "easemytrip", "IndiGo", "ECONOMY", "2026-09-15", False, "₹6,000", timestamp, "extracted", 0, "url"),
    ]
    weights = Weights(route_weights={"DEL-BOM": 1.0})

    report = calculate_apix_report(obs, weights)

    assert report["calculation_status"] == "BLOCKED"
    assert report["reason"] == "MISSING_GENUINE_BASE_PERIOD"


def test_identical_snapshot_copied_across_periods_blocked():
    """Verify that copying a current snapshot into base is BLOCKED."""
    ts_base = "2026-08-28T08:00:00Z"
    ts_current = "2026-08-28T08:01:00Z"
    # Identical fares and identical observation ID structure
    obs = [
        Observation("easemytrip-current-2026-09-15-DEL-BOM-1", "base", "DEL-BOM", "DEL", "BOM", 15, 6000.0, "easemytrip", "IndiGo", "ECONOMY", "2026-09-15", False, "₹6,000", ts_base, "extracted", 0, "url"),
        Observation("easemytrip-current-2026-09-15-DEL-BOM-1", "current", "DEL-BOM", "DEL", "BOM", 15, 6000.0, "easemytrip", "IndiGo", "ECONOMY", "2026-09-15", False, "₹6,000", ts_current, "extracted", 0, "url"),
    ]
    weights = Weights(route_weights={"DEL-BOM": 1.0})

    report = calculate_apix_report(obs, weights)

    assert report["calculation_status"] == "BLOCKED"
    assert report["reason"] == "MISSING_GENUINE_BASE_PERIOD"


def test_missing_base_period_blocked():
    """Verify that having only CURRENT period observations returns BLOCKED."""
    obs = [
        Observation("easemytrip-current-1", "current", "DEL-BOM", "DEL", "BOM", 15, 6000.0, "easemytrip", "IndiGo", "ECONOMY", "2026-09-15", False, "₹6,000", "2026-08-28T08:00:00Z", "extracted", 0, "url"),
    ]
    weights = Weights(route_weights={"DEL-BOM": 1.0})

    report = calculate_apix_report(obs, weights)

    assert report["calculation_status"] == "BLOCKED"
    assert report["reason"] == "MISSING_GENUINE_BASE_PERIOD"


def test_missing_route_weights_returns_missing_input():
    """Verify that when official route weights are unconfigured, weighting status is MISSING_INPUT or ROUTE_WEIGHTS_MISSING."""
    base_obs = [
        Observation("b1", "base", "DEL-BOM", "DEL", "BOM", 15, 5000.0, "easemytrip", "IndiGo", "ECONOMY", "2026-08-01", False, "5000", "2026-08-01T08:00:00Z", "extracted", 0, "url"),
    ]
    current_obs = [
        Observation("c1", "current", "DEL-BOM", "DEL", "BOM", 15, 5500.0, "easemytrip", "IndiGo", "ECONOMY", "2026-09-01", False, "5500", "2026-09-01T08:00:00Z", "extracted", 0, "url"),
    ]
    # Empty route weights
    empty_weights = Weights(route_weights={})

    with pytest.raises(ValueError, match="Authoritative route weights"):
        calculate_apix_report(base_obs + current_obs, empty_weights)


def test_multiple_historical_snapshots_selects_latest_run():
    """Verify that when multiple historical collection runs exist, select_latest_snapshots picks the latest timestamps for base and current."""
    old_base = Observation("b-old", "base", "DEL-BOM", "DEL", "BOM", 15, 4500.0, "easemytrip", "IndiGo", "ECONOMY", "2026-07-01", False, "4500", "2026-07-01T08:00:00Z", "extracted", 0, "url")
    latest_base = Observation("b-new", "base", "DEL-BOM", "DEL", "BOM", 15, 5000.0, "easemytrip", "IndiGo", "ECONOMY", "2026-08-01", False, "5000", "2026-08-01T08:00:00Z", "extracted", 0, "url")

    old_current = Observation("c-old", "current", "DEL-BOM", "DEL", "BOM", 15, 5200.0, "easemytrip", "IndiGo", "ECONOMY", "2026-08-15", False, "5200", "2026-08-15T08:00:00Z", "extracted", 0, "url")
    latest_current = Observation("c-new", "current", "DEL-BOM", "DEL", "BOM", 15, 5500.0, "easemytrip", "IndiGo", "ECONOMY", "2026-09-01", False, "5500", "2026-09-01T08:00:00Z", "extracted", 0, "url")

    all_obs = [old_base, latest_base, old_current, latest_current]

    selected = select_latest_snapshots(all_obs)
    selected_ids = {o.observation_id for o in selected}

    assert "b-new" in selected_ids
    assert "c-new" in selected_ids
    assert "b-old" not in selected_ids
    assert "c-old" not in selected_ids
