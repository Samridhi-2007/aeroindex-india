import csv
import math
from pathlib import Path

from .models import Observation, WeightMetadata, Weights

REQUIRED_COLUMNS = {"observation_id", "period", "route", "origin", "destination", "booking_window_days", "total_consumer_fare", "source_id", "carrier", "fare_class", "observation_date", "is_duplicate"}


def load_observations(path: str | Path) -> list[Observation]:
    """Load CSV observations, preserving invalid fares as missing values."""
    with Path(path).open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames or not REQUIRED_COLUMNS.issubset(reader.fieldnames):
            raise ValueError("Dataset is missing one or more required columns")
        result = []
        for row in reader:
            try:
                fare = float(row["total_consumer_fare"])
                if not math.isfinite(fare):
                    fare = None
            except (TypeError, ValueError):
                fare = None
            result.append(Observation(row["observation_id"], row["period"], row["route"], row["origin"], row["destination"], int(row["booking_window_days"]), fare, row["source_id"], row["carrier"], row["fare_class"], row["observation_date"], row["is_duplicate"].strip().lower() == "true"))
    return result


def load_weights(path: str | Path) -> Weights:
    """Load route and booking-window weights from CSV (supports standard and official-derived schemas)."""
    routes: dict[str, float] = {}
    windows: dict[int, float] = {}
    route_metadata: dict[str, WeightMetadata] = {}
    window_metadata: dict[int, WeightMetadata] = {}
    with Path(path).open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        fieldnames = set(reader.fieldnames or [])
        for row in reader:
            if "route" in fieldnames and "weight" in fieldnames:
                route_key = row["route"]
                try:
                    value = float(row["weight"])
                except (TypeError, ValueError) as error:
                    raise ValueError(f"Invalid route weight value for {route_key}") from error
                routes[route_key] = value
                source = row.get("source", "DGCA")
                status = row.get("provenance_status", "official_data_derived")
                ref = f"{row.get('publication', '')} ({row.get('reference_year', '')})"
                route_metadata[route_key] = WeightMetadata(source, status, ref)
            else:
                try:
                    value = float(row["value"])
                except (TypeError, ValueError) as error:
                    raise ValueError(f"Invalid weight value for {row.get('key')}") from error
                if row["type"] == "route_weight":
                    routes[row["key"]] = value
                    route_metadata[row["key"]] = WeightMetadata(str(path), "demonstration" if "demo" in row.get("note", "").lower() else "configured", row.get("note", ""))
                elif row["type"] == "window_weight":
                    windows[int(row["key"])] = value
                    window_metadata[int(row["key"])] = WeightMetadata(str(path), "demonstration" if "demo" in row.get("note", "").lower() else "configured", row.get("note", ""))
    return Weights(routes, windows, route_weight_metadata=route_metadata, window_weight_metadata=window_metadata)



def load_cpi_airfare_weight(path: str | Path, sector: str = "Combined", state: str = "All India") -> Weights:
    """Load the official CPI Airfare item weight without inventing route/window weights."""
    with Path(path).open(newline="", encoding="utf-8-sig") as file:
        rows = csv.DictReader(file)
        matches = [row for row in rows if row.get("item") == "Airfare" and row.get("sector") == sector and row.get("state") == state and row.get("weight")]
    if not matches:
        raise ValueError("No CPI Airfare weight found for the requested sector and state")
    weight = float(matches[0]["weight"])
    return Weights(airfare_weight=weight, airfare_weight_metadata=WeightMetadata(str(path), "official", "CPI 2024 Airfare item weight"))