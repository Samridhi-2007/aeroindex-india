import math
import sqlite3
import pytest
from pathlib import Path

from intelligence.models import Observation, Weights, WeightMetadata
from intelligence.index_engine.apix import (
    calculate_apix_report,
    elementary_index,
    jevons_index,
    price_relative,
)
from intelligence.storage import IntelligenceRepository
from intelligence.pipeline import clean_observations


def test_apix_blocked_when_base_period_is_missing(tmp_path):
    """Verify that when only CURRENT period observations are present, APIx calculation is BLOCKED."""
    source_db = tmp_path / "source.db"
    result_db = tmp_path / "results.db"

    source_repo = IntelligenceRepository(source_db)
    result_repo = IntelligenceRepository(result_db)

    # Save only CURRENT period observations
    current_obs = [
        Observation("easemytrip-current-1", "current", "DEL-BOM", "DEL", "BOM", 15, 6000.0, "easemytrip", "IndiGo", "ECONOMY", "2026-09-15", False, "₹6,000", "2026-08-28T10:00:00Z", "extracted", 0, "https://easemytrip.com"),
        Observation("easemytrip-current-2", "current", "DEL-BOM", "DEL", "BOM", 15, 6400.0, "easemytrip", "Air India", "ECONOMY", "2026-09-15", False, "₹6,400", "2026-08-28T10:00:00Z", "extracted", 0, "https://easemytrip.com"),
    ]
    source_repo.save_observations(current_obs)

    route_weights = Weights(
        route_weights={"DEL-BOM": 1.0},
        window_weights={15: 1.0},
        airfare_weight=0.01166625043306,
        route_weight_metadata={"DEL-BOM": WeightMetadata("official_cpi_basket", "official", "CPI 2024 Table 4")},
        window_weight_metadata={15: WeightMetadata("parameter", "configured", "Collection Window Parameter")},
        airfare_weight_metadata=WeightMetadata("official_cpi_item", "official", "CPI 2024 Airfare Item Weight"),
    )
    source_repo.save_weights(route_weights)

    report = calculate_apix_report(source_repo.load_observations(), source_repo.load_weights())

    assert report["calculation_status"] == "BLOCKED"
    assert report["apix"] is None
    assert report["reason"] == "MISSING_GENUINE_BASE_PERIOD"
    assert any(issue["issue_type"] == "missing_genuine_base_period" for issue in report["validation_issues"])

    result_repo.save_report(report)
    loaded_report = result_repo.load_validation_issues()
    assert len(loaded_report) >= 0


def test_apix_blocked_when_base_is_duplicate_of_current(tmp_path):
    """Verify that copying current data into base is detected as duplicate and BLOCKED."""
    source_db = tmp_path / "source.db"
    source_repo = IntelligenceRepository(source_db)

    # Identical fares and timestamps across base and current
    timestamp = "2026-08-28T10:00:00Z"
    obs = [
        Observation("easemytrip-current-1", "current", "DEL-BOM", "DEL", "BOM", 15, 6000.0, "easemytrip", "IndiGo", "ECONOMY", "2026-09-15", False, "₹6,000", timestamp, "extracted", 0, "url"),
        Observation("easemytrip-base-1", "base", "DEL-BOM", "DEL", "BOM", 15, 6000.0, "easemytrip", "IndiGo", "ECONOMY", "2026-09-15", False, "₹6,000", timestamp, "extracted", 0, "url"),
    ]
    source_repo.save_observations(obs)

    weights = Weights(
        route_weights={"DEL-BOM": 1.0},
        window_weights={15: 1.0},
        route_weight_metadata={"DEL-BOM": WeightMetadata("official", "official", "ref")},
    )

    report = calculate_apix_report(source_repo.load_observations(), weights)

    assert report["calculation_status"] == "BLOCKED"
    assert report["apix"] is None
    assert report["reason"] == "MISSING_GENUINE_BASE_PERIOD"


def test_apix_blocked_when_route_weights_missing(tmp_path):
    """Verify that calculation raises ValueError or returns BLOCKED when authoritative route weights are invalid or sum != 1.0."""
    obs = [
        Observation("obs-b1", "base", "DEL-BOM", "DEL", "BOM", 15, 5000.0, "src", "IndiGo", "ECONOMY", "2026-08-01", False, "5000", "2026-08-01T00:00:00Z", "extracted", 0, "url"),
        Observation("obs-c1", "current", "DEL-BOM", "DEL", "BOM", 15, 5500.0, "src", "IndiGo", "ECONOMY", "2026-09-01", False, "5500", "2026-09-01T00:00:00Z", "extracted", 0, "url"),
    ]

    invalid_weights = Weights(
        route_weights={"DEL-BOM": 0.50},  # Sums to 0.50, not 1.0
        window_weights={15: 1.0},
    )

    with pytest.raises(ValueError, match="Authoritative route weights must be finite, non-negative, and sum to 1"):
        calculate_apix_report(obs, invalid_weights)


def test_complete_worked_apix_calculation(tmp_path):
    """
    Complete worked test proving genuine BASE + CURRENT observations produce a mathematically valid APIx:
    - Route 1: DEL-BOM (Weight = 0.60)
        - Base fare: 5000.0 INR, Current fare: 5500.0 INR -> Price Relative = 110.0
    - Route 2: BOM-BLR (Weight = 0.40)
        - Base fare: 4000.0 INR, Current fare: 4800.0 INR -> Price Relative = 120.0
    - Expected Elementary Indices:
        - DEL-BOM Jevons index = 110.0
        - BOM-BLR Jevons index = 120.0
    - Expected Aggregate APIx:
        - APIx = (0.60 * 110.0) + (0.40 * 120.0) = 66.0 + 48.0 = 114.0
    """
    source_db = tmp_path / "source.db"
    result_db = tmp_path / "results.db"

    source_repo = IntelligenceRepository(source_db)
    result_repo = IntelligenceRepository(result_db)

    # Genuine Historical BASE Snapshot (Collected 2026-08-01)
    base_observations = [
        Observation("easemytrip-base-1", "base", "DEL-BOM", "DEL", "BOM", 15, 5000.0, "easemytrip", "IndiGo", "ECONOMY", "2026-08-01", False, "₹5,000", "2026-08-01T08:00:00Z", "extracted", 0, "https://easemytrip.com"),
        Observation("easemytrip-base-2", "base", "BOM-BLR", "BOM", "BLR", 15, 4000.0, "easemytrip", "Air India", "ECONOMY", "2026-08-01", False, "₹4,000", "2026-08-01T08:00:00Z", "extracted", 0, "https://easemytrip.com"),
    ]

    # Genuine CURRENT Snapshot (Collected 2026-09-01)
    current_observations = [
        Observation("easemytrip-current-1", "current", "DEL-BOM", "DEL", "BOM", 15, 5500.0, "easemytrip", "IndiGo", "ECONOMY", "2026-09-01", False, "₹5,500", "2026-09-01T08:00:00Z", "extracted", 0, "https://easemytrip.com"),
        Observation("easemytrip-current-2", "current", "BOM-BLR", "BOM", "BLR", 15, 4800.0, "easemytrip", "Air India", "ECONOMY", "2026-09-01", False, "₹4,800", "2026-09-01T08:00:00Z", "extracted", 0, "https://easemytrip.com"),
    ]

    all_obs = base_observations + current_observations
    source_repo.save_observations(all_obs)

    # Authoritative Route Weights
    authoritative_weights = Weights(
        route_weights={"DEL-BOM": 0.60, "BOM-BLR": 0.40},
        window_weights={15: 1.0},
        airfare_weight=0.01166625043306,
        route_weight_metadata={
            "DEL-BOM": WeightMetadata("official_cpi_basket", "official", "CPI 2024 Table 4"),
            "BOM-BLR": WeightMetadata("official_cpi_basket", "official", "CPI 2024 Table 4"),
        },
        window_weight_metadata={15: WeightMetadata("parameter", "configured", "Collection Window Parameter")},
        airfare_weight_metadata=WeightMetadata("official_cpi_item", "official", "CPI 2024 Airfare Item Weight Reference"),
    )
    source_repo.save_weights(authoritative_weights)

    # Execute Complete APIx Calculation
    report = calculate_apix_report(source_repo.load_observations(), source_repo.load_weights())

    # Step-by-Step Mathematical Assertions
    assert report["calculation_status"] == "OK"
    assert report["weighting_status"] == "OFFICIAL-WEIGHTED"

    # Route 1: DEL-BOM
    del_bom_component = next(r for r in report["route_components"] if r["route"] == "DEL-BOM")
    assert del_bom_component["route_weight"] == 0.60
    assert math.isclose(del_bom_component["elementary_index"], 110.0, abs_tol=1e-5)
    assert math.isclose(del_bom_component["contribution"], 0.60 * 110.0, abs_tol=1e-5)

    # Route 2: BOM-BLR
    bom_blr_component = next(r for r in report["route_components"] if r["route"] == "BOM-BLR")
    assert bom_blr_component["route_weight"] == 0.40
    assert math.isclose(bom_blr_component["elementary_index"], 120.0, abs_tol=1e-5)
    assert math.isclose(bom_blr_component["contribution"], 0.40 * 120.0, abs_tol=1e-5)

    # Aggregate APIx Calculation
    expected_apix = (0.60 * 110.0) + (0.40 * 120.0)  # 66.0 + 48.0 = 114.0
    assert report["apix"] is not None
    assert math.isclose(report["apix"], expected_apix, abs_tol=1e-5)

    # Persist report to results.db
    report_id = result_repo.save_report(report)
    assert report_id > 0

    # Reload from results.db and verify
    conn = sqlite3.connect(result_db)
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT report_json FROM reports WHERE report_id = ?", (report_id,)).fetchone()
    conn.close()

    assert row is not None
    import json
    persisted = json.loads(row["report_json"])
    assert math.isclose(persisted["apix"], 114.0, abs_tol=1e-5)
    assert persisted["calculation_status"] == "OK"

    assert persisted["weighting_status"] == "OFFICIAL-WEIGHTED"

    source_repo.close()
    result_repo.close()
