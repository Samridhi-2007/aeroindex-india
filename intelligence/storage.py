import json
import sqlite3
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from .models import Observation, RawFareObservation, WeightMetadata, Weights


class IntelligenceRepository:
    """SQLite persistence for collected observations, weights, and reports."""

    def __init__(self, path: str | Path = "data/intelligence.db") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.path)
        self.connection.row_factory = sqlite3.Row
        self._create_schema()

    def _create_schema(self) -> None:
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS observations (
                observation_id TEXT PRIMARY KEY,
                period TEXT NOT NULL,
                route TEXT NOT NULL,
                origin TEXT NOT NULL,
                destination TEXT NOT NULL,
                booking_window_days INTEGER NOT NULL,
                total_consumer_fare REAL,
                source_id TEXT NOT NULL,
                carrier TEXT NOT NULL,
                fare_class TEXT NOT NULL,
                observation_date TEXT NOT NULL,
                is_duplicate INTEGER NOT NULL
                ,raw_fare TEXT, collection_timestamp TEXT, extraction_status TEXT, stops INTEGER, source_url TEXT
            );
            CREATE TABLE IF NOT EXISTS raw_observations (
                observation_id TEXT PRIMARY KEY, period TEXT NOT NULL, route TEXT NOT NULL,
                origin TEXT NOT NULL, destination TEXT NOT NULL, booking_window_days INTEGER NOT NULL,
                raw_fare TEXT, source_id TEXT NOT NULL, carrier TEXT, fare_class TEXT,
                observation_date TEXT NOT NULL, collection_timestamp TEXT NOT NULL,
                extraction_status TEXT NOT NULL, stops INTEGER, source_url TEXT
            );
            CREATE TABLE IF NOT EXISTS validation_issues (
                issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
                observation_id TEXT NOT NULL,
                issue_type TEXT NOT NULL,
                detail TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS weights (
                weight_type TEXT NOT NULL,
                weight_key TEXT NOT NULL,
                value REAL NOT NULL,
                PRIMARY KEY (weight_type, weight_key)
            );
            CREATE TABLE IF NOT EXISTS weight_metadata (
                weight_type TEXT NOT NULL,
                weight_key TEXT NOT NULL,
                source TEXT NOT NULL,
                status TEXT NOT NULL,
                reference TEXT NOT NULL,
                PRIMARY KEY (weight_type, weight_key)
            );
            CREATE TABLE IF NOT EXISTS reports (
                report_id INTEGER PRIMARY KEY AUTOINCREMENT,
                generated_at TEXT NOT NULL,
                base_period TEXT NOT NULL,
                current_period TEXT NOT NULL,
                report_json TEXT NOT NULL
            );
            """
        )
        for column, definition in (("raw_fare", "TEXT"), ("collection_timestamp", "TEXT"), ("extraction_status", "TEXT"), ("stops", "INTEGER"), ("source_url", "TEXT")):
            try:
                self.connection.execute(f"ALTER TABLE observations ADD COLUMN {column} {definition}")
            except sqlite3.OperationalError:
                pass
        self.connection.commit()

    def save_raw_observations(self, observations: list[RawFareObservation]) -> None:
        self.connection.executemany(
            "INSERT OR REPLACE INTO raw_observations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [(item.observation_id, item.period, item.route, item.origin, item.destination, item.booking_window_days, item.raw_fare, item.source_id, item.carrier, item.fare_class, item.observation_date, item.collection_timestamp, item.extraction_status, item.stops, item.source_url) for item in observations],
        )
        self.connection.commit()

    def save_validation_issues(self, issues: list[dict[str, str]]) -> None:
        self.connection.executemany(
            "INSERT INTO validation_issues (observation_id, issue_type, detail, created_at) VALUES (?, ?, ?, ?)",
            [(issue["observation_id"], issue["issue_type"], issue["detail"], datetime.now(timezone.utc).isoformat()) for issue in issues],
        )
        self.connection.commit()

    def load_validation_issues(self) -> list[dict[str, str]]:
        return [dict(row) for row in self.connection.execute("SELECT observation_id, issue_type, detail, created_at FROM validation_issues ORDER BY issue_id")]

    def save_observations(self, observations: list[Observation]) -> None:
        self.connection.executemany(
            """
            INSERT OR REPLACE INTO observations
            (observation_id, period, route, origin, destination, booking_window_days,
             total_consumer_fare, source_id, carrier, fare_class, observation_date,
             is_duplicate, raw_fare, collection_timestamp, extraction_status, stops, source_url) VALUES
            (:observation_id, :period, :route, :origin, :destination,
             :booking_window_days, :total_consumer_fare, :source_id, :carrier,
             :fare_class, :observation_date, :is_duplicate, :raw_fare,
             :collection_timestamp, :extraction_status, :stops, :source_url)
            """,
            [{**asdict(item), "is_duplicate": int(item.is_duplicate)} for item in observations],
        )
        self.connection.commit()

    def load_observations(self) -> list[Observation]:
        rows = self.connection.execute("SELECT * FROM observations ORDER BY observation_id").fetchall()
        return [Observation(**{**dict(row), "is_duplicate": bool(row["is_duplicate"]), "extraction_status": row["extraction_status"] or "normalized"}) for row in rows]

    def save_weights(self, weights: Weights) -> None:
        rows = [("route_weight", key, value) for key, value in weights.route_weights.items()]
        rows += [("window_weight", str(key), value) for key, value in weights.window_weights.items()]
        if weights.airfare_weight is not None:
            rows.append(("airfare_weight", "airfare", weights.airfare_weight))
        self.connection.executemany("INSERT OR REPLACE INTO weights VALUES (?, ?, ?)", rows)
        metadata = [("route_weight", key, value.source, value.status, value.reference) for key, value in weights.route_weight_metadata.items()]
        metadata += [("window_weight", str(key), value.source, value.status, value.reference) for key, value in weights.window_weight_metadata.items()]
        if weights.airfare_weight_metadata:
            value = weights.airfare_weight_metadata
            metadata.append(("airfare_weight", "airfare", value.source, value.status, value.reference))
        self.connection.executemany("INSERT OR REPLACE INTO weight_metadata VALUES (?, ?, ?, ?, ?)", metadata)
        self.connection.commit()

    def load_weights(self) -> Weights:
        rows = self.connection.execute("SELECT weight_type, weight_key, value FROM weights").fetchall()
        routes = {row["weight_key"]: row["value"] for row in rows if row["weight_type"] == "route_weight"}
        windows = {int(row["weight_key"]): row["value"] for row in rows if row["weight_type"] == "window_weight"}
        airfare = next((row["value"] for row in rows if row["weight_type"] == "airfare_weight"), None)
        metadata = self.connection.execute("SELECT * FROM weight_metadata").fetchall()
        route_metadata = {row["weight_key"]: WeightMetadata(row["source"], row["status"], row["reference"]) for row in metadata if row["weight_type"] == "route_weight"}
        window_metadata = {int(row["weight_key"]): WeightMetadata(row["source"], row["status"], row["reference"]) for row in metadata if row["weight_type"] == "window_weight"}
        airfare_metadata_row = next((row for row in metadata if row["weight_type"] == "airfare_weight"), None)
        airfare_metadata = WeightMetadata(airfare_metadata_row["source"], airfare_metadata_row["status"], airfare_metadata_row["reference"]) if airfare_metadata_row else None
        return Weights(routes, windows, airfare, route_metadata, window_metadata, airfare_metadata)

    def save_report(self, report: dict, base_period: str = "base", current_period: str = "current") -> int:
        cursor = self.connection.execute(
            "INSERT INTO reports (generated_at, base_period, current_period, report_json) VALUES (?, ?, ?, ?)",
            (datetime.now(timezone.utc).isoformat(), base_period, current_period, json.dumps(report)),
        )
        self.connection.commit()
        return int(cursor.lastrowid)

    def close(self) -> None:
        self.connection.close()