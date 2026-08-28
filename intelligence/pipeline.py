from collections.abc import Iterable
from typing import Protocol

from .index_engine.apix import calculate_apix_report
import math
import re

from .models import Observation, RawFareObservation
from .storage import IntelligenceRepository


class FareCollector(Protocol):
    source_id: str

    def collect(self) -> Iterable[Observation]:
        """Collect normalized observations from one source."""


def _raw_from_observation(item: Observation) -> RawFareObservation:
    return RawFareObservation(item.observation_id, item.period, item.route, item.origin, item.destination, item.booking_window_days, item.raw_fare, item.source_id or "", item.carrier, item.fare_class, item.observation_date, item.collection_timestamp or "", item.extraction_status, item.stops, item.source_url)


def clean_observations(observations: Iterable[Observation | RawFareObservation]) -> list[Observation]:
    """Normalize fields and discard structurally invalid rows before persistence."""
    cleaned: list[Observation] = []
    seen_ids: set[str] = set()
    for raw_item in observations:
        item = _raw_from_observation(raw_item) if isinstance(raw_item, Observation) else raw_item
        observation_id = item.observation_id.strip()
        period = item.period.strip().lower()
        route = item.route.strip().upper()
        origin = item.origin.strip().upper()
        destination = item.destination.strip().upper()
        source_id = item.source_id.strip().lower()
        carrier = item.carrier.strip() if item.carrier else "UNSPECIFIED"
        fare_class = item.fare_class.strip().upper() if item.fare_class else "ECONOMY"
        if not observation_id or not period or not route or not origin or not destination or not source_id:
            continue
        if item.booking_window_days <= 0 or observation_id in seen_ids:
            continue
        seen_ids.add(observation_id)
        match = re.search(r"(?:INR|Rs\.?|₹|\u20b9)?\s*([\d,]+(?:\.\d+)?)", item.raw_fare or "", re.IGNORECASE)
        cleaned_fare = float(match.group(1).replace(",", "")) if match else None
        if cleaned_fare is None and isinstance(raw_item, Observation):
            cleaned_fare = raw_item.total_consumer_fare
        cleaned.append(Observation(observation_id, period, route, origin, destination, item.booking_window_days, cleaned_fare, source_id, carrier, fare_class, item.observation_date.strip(), False, item.raw_fare, item.collection_timestamp or None, item.extraction_status if cleaned_fare is not None else "invalid_fare", item.stops, item.source_url))
    return cleaned


def clean_observations_with_report(observations: Iterable[Observation | RawFareObservation]) -> tuple[list[Observation], list[dict[str, str]]]:
    issues: list[dict[str, str]] = []
    items = list(observations)
    cleaned: list[Observation] = []
    seen_ids: set[str] = set()
    for raw_item in items:
        item = _raw_from_observation(raw_item) if isinstance(raw_item, Observation) else raw_item
        if not item.observation_id.strip():
            issues.append({"observation_id": item.observation_id, "issue_type": "missing_observation_id", "detail": "Observation ID is required"})
            continue
        if item.observation_id.strip() in seen_ids:
            issues.append({"observation_id": item.observation_id, "issue_type": "duplicate_observation", "detail": "Duplicate observation ID"})
            continue
        seen_ids.add(item.observation_id.strip())
        normalized = clean_observations([raw_item])
        if not normalized:
            issues.append({"observation_id": item.observation_id, "issue_type": "invalid_structure", "detail": "Required fields or booking window are invalid"})
            continue
        observation = normalized[0]
        if observation.total_consumer_fare is None:
            issues.append({"observation_id": observation.observation_id, "issue_type": "invalid_fare", "detail": "Fare is missing, non-numeric, non-finite, or non-positive"})
        cleaned.append(observation)
    return cleaned, issues


def collect_and_calculate(source_repository: IntelligenceRepository, result_repository: IntelligenceRepository, collectors: Iterable[FareCollector]) -> dict:
    """Persist fares in the source DB, calculate from that DB, and persist the report in the result DB."""
    cleaning_issues: list[dict[str, str]] = []
    for collector in collectors:
        collected = list(collector.collect())
        raw_observations = [_raw_from_observation(item) if isinstance(item, Observation) else item for item in collected]
        source_repository.save_raw_observations(raw_observations)
        cleaned, issues = clean_observations_with_report(collected)
        if not collected:
            issues.append({"observation_id": collector.source_id, "issue_type": "no_fares_extracted", "detail": "Collector returned no fare observations"})
        source_repository.save_observations(cleaned)
        source_repository.save_validation_issues(issues)
        cleaning_issues.extend(issues)
    try:
        report = calculate_apix_report(source_repository.load_observations(), source_repository.load_weights())
    except ValueError as error:
        if "Authoritative route weights" not in str(error):
            raise
        report = {"apix": None, "base": 100.0, "index_name": "Airfare Price Index", "calculation_status": "BLOCKED", "weighting_status": "ROUTE_WEIGHTS_MISSING", "methodology": "CPI 2024 / Jevons elementary indices aggregated with authoritative route weights", "validation_issues": [{"issue_type": "missing_route_weights", "detail": str(error)}], "components": [], "route_components": [], "booking_window_components": [], "insights": []}
    report["validation_issues"] = cleaning_issues + report.get("validation_issues", [])
    result_repository.save_report(report)
    return report