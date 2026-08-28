import pytest

from intelligence.models import Observation, RawFareObservation, Weights
from intelligence.airline_collectors import EaseMyTripCollector, SkyscannerCollector
from intelligence.pipeline import clean_observations, clean_observations_with_report, collect_and_calculate
from intelligence.storage import IntelligenceRepository


def test_repository_round_trips_observations_weights_and_report(tmp_path):
    repository = IntelligenceRepository(tmp_path / "intelligence.db")
    observation = Observation("1", "base", "R", "A", "B", 1, 100, "source", "C", "E", "2026-01-01", False)
    weights = Weights({"R": 1.0}, {1: 1.0})

    repository.save_observations([observation])
    repository.save_weights(weights)
    report_id = repository.save_report({"apix": 100})

    assert repository.load_observations() == [observation]
    assert repository.load_weights() == weights
    assert report_id == 1
    repository.close()


class Collector:
    source_id = "indigo"

    def __init__(self, observations):
        self.observations = observations

    def collect(self):
        return self.observations


def test_pipeline_separates_source_and_result_databases(tmp_path):
    source = IntelligenceRepository(tmp_path / "source.db")
    results = IntelligenceRepository(tmp_path / "results.db")
    source.save_weights(Weights({"R": 1.0}, {1: 1.0}))
    observations = [
        Observation("base", "base", "R", "A", "B", 1, 100, "indigo", "IndiGo", "E", "2026-01-01", False),
        Observation("current", "current", "R", "A", "B", 1, 120, "indigo", "IndiGo", "E", "2026-01-02", False),
    ]

    report = collect_and_calculate(source, results, [Collector(observations)])

    assert report["apix"] == pytest.approx(120)
    assert source.load_observations() == observations
    assert results.connection.execute("SELECT COUNT(*) FROM reports").fetchone()[0] == 1
    assert source.connection.execute("SELECT COUNT(*) FROM reports").fetchone()[0] == 0
    raw_row = source.connection.execute("SELECT raw_fare, extraction_status FROM raw_observations WHERE observation_id = 'base'").fetchone()
    assert (raw_row[0], raw_row[1]) == (None, "normalized")
    source.close()
    results.close()


def test_clean_observations_normalizes_and_drops_invalid_rows():
    observations = [
        Observation(" 1 ", " BASE ", "r", "a", "b", 1, 100, " INDIGO ", " IndiGo ", " economy ", "2026-01-01", False),
        Observation("1", "base", "R", "A", "B", 1, 100, "indigo", "IndiGo", "E", "2026-01-01", False),
        Observation("", "base", "R", "A", "B", 1, 100, "indigo", "IndiGo", "E", "2026-01-01", False),
    ]

    assert clean_observations(observations) == [
        Observation("1", "base", "R", "A", "B", 1, 100, "indigo", "IndiGo", "ECONOMY", "2026-01-01", False)
    ]


def test_raw_fare_is_cleaned_without_losing_source_value():
    raw = RawFareObservation("1", "current", "R", "A", "B", 15, "Book with Air India from ₹6,580", "skyscanner", "Air India", "ECONOMY", "2026-09-15", "2026-08-27T00:00:00+00:00")
    cleaned, issues = clean_observations_with_report([raw])
    assert cleaned[0].total_consumer_fare == 6580
    assert cleaned[0].raw_fare == "Book with Air India from ₹6,580"
    assert issues == []


def test_pipeline_reports_missing_route_weights(tmp_path):
    source = IntelligenceRepository(tmp_path / "source.db")
    results = IntelligenceRepository(tmp_path / "results.db")
    report = collect_and_calculate(source, results, [Collector([])])
    assert report["calculation_status"] == "BLOCKED"
    assert report["weighting_status"] == "ROUTE_WEIGHTS_MISSING"
    source.close()
    results.close()


def test_skyscanner_collector_builds_direct_results_url():
    collector = SkyscannerCollector("DEL", "BOM", "2026-09-15", "current", 15, ".fare-card")
    assert collector.booking_url == "https://www.skyscanner.co.in/transport/flights/del/bom/20260915/?adultsv2=1&cabinclass=economy&currency=INR&market=IN&rtn=0"


def test_skyscanner_collector_uses_live_fare_text_selector_by_default():
    collector = SkyscannerCollector("DEL", "BOM", "2026-09-15", "current", 15)
    assert collector.fare_selector == '[data-backpack-ds-component="Text"]'


def test_easemytrip_collector_builds_listing_url_and_uses_value_selector():
    collector = EaseMyTripCollector("DEL", "BOM", "2026-09-15", "current", 15)
    assert collector.fare_selector == ".value"
    assert "DEL-Delhi-India|BOM-Mumbai-India|15/09/2026" in collector.booking_url


def test_easemytrip_fare_text_is_normalized_by_shared_extractor():
    class Locator:
        def all_inner_texts(self):
            return ["₹6,408", "Book now ₹6,530"]

    class Page:
        def locator(self, selector):
            assert selector == ".value"
            return Locator()

    fares = EaseMyTripCollector("DEL", "BOM", "2026-09-15", "current", 15).read_fares(Page())
    assert fares == [("₹6,408", 6408.0), ("Book now ₹6,530", 6530.0)]