import json
import os
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any

from .models import Observation, RawFareObservation, WeightMetadata, Weights


class MySQLRepository:
    """MySQL implementation of the source/result repository contract."""

    def __init__(self, database: str, host: str = "127.0.0.1", port: int = 3306, user: str = "root", password: str | None = None) -> None:
        try:
            import mysql.connector
        except ImportError as error:
            raise RuntimeError("Install mysql-connector-python") from error
        self.database = database
        self.connection = mysql.connector.connect(host=host, port=port, user=user, password=password if password is not None else os.getenv("MYSQL_PASSWORD"), database=database)
        self._create_schema()

    def _create_schema(self) -> None:
        statements = (
            """CREATE TABLE IF NOT EXISTS raw_observations (observation_id VARCHAR(255) PRIMARY KEY, period VARCHAR(32) NOT NULL, route VARCHAR(32) NOT NULL, origin VARCHAR(16) NOT NULL, destination VARCHAR(16) NOT NULL, booking_window_days INT NOT NULL, raw_fare TEXT, source_id VARCHAR(64) NOT NULL, carrier VARCHAR(128), fare_class VARCHAR(64), observation_date VARCHAR(32) NOT NULL, collection_timestamp VARCHAR(64) NOT NULL, extraction_status VARCHAR(64) NOT NULL, stops INT, source_url TEXT)""",
            """CREATE TABLE IF NOT EXISTS observations (observation_id VARCHAR(255) PRIMARY KEY, period VARCHAR(32) NOT NULL, route VARCHAR(32) NOT NULL, origin VARCHAR(16) NOT NULL, destination VARCHAR(16) NOT NULL, booking_window_days INT NOT NULL, total_consumer_fare DECIMAL(12,2), source_id VARCHAR(64) NOT NULL, carrier VARCHAR(128), fare_class VARCHAR(64), observation_date VARCHAR(32) NOT NULL, is_duplicate BOOLEAN NOT NULL, raw_fare TEXT, collection_timestamp VARCHAR(64), extraction_status VARCHAR(64), stops INT, source_url TEXT)""",
            """CREATE TABLE IF NOT EXISTS validation_issues (issue_id BIGINT AUTO_INCREMENT PRIMARY KEY, observation_id VARCHAR(255) NOT NULL, issue_type VARCHAR(128) NOT NULL, detail TEXT NOT NULL, created_at VARCHAR(64) NOT NULL)""",
            """CREATE TABLE IF NOT EXISTS weights (weight_type VARCHAR(64) NOT NULL, weight_key VARCHAR(255) NOT NULL, value DECIMAL(20,12) NOT NULL, PRIMARY KEY (weight_type, weight_key))""",
            """CREATE TABLE IF NOT EXISTS weight_metadata (weight_type VARCHAR(64) NOT NULL, weight_key VARCHAR(255) NOT NULL, source TEXT NOT NULL, status VARCHAR(64) NOT NULL, reference TEXT NOT NULL, PRIMARY KEY (weight_type, weight_key))""",
            """CREATE TABLE IF NOT EXISTS reports (report_id BIGINT AUTO_INCREMENT PRIMARY KEY, generated_at VARCHAR(64) NOT NULL, base_period VARCHAR(32) NOT NULL, current_period VARCHAR(32) NOT NULL, report_json JSON NOT NULL)""",
        )
        cursor = self.connection.cursor()
        for statement in statements:
            cursor.execute(statement)
        self.connection.commit()
        cursor.close()

    def _executemany(self, statement: str, rows: list[tuple[Any, ...]]) -> None:
        if rows:
            cursor = self.connection.cursor()
            cursor.executemany(statement, rows)
            self.connection.commit()
            cursor.close()

    def save_raw_observations(self, observations: list[RawFareObservation]) -> None:
        self._executemany("INSERT INTO raw_observations VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE raw_fare=VALUES(raw_fare), extraction_status=VALUES(extraction_status)", [(item.observation_id, item.period, item.route, item.origin, item.destination, item.booking_window_days, item.raw_fare, item.source_id, item.carrier, item.fare_class, item.observation_date, item.collection_timestamp, item.extraction_status, item.stops, item.source_url) for item in observations])

    def save_observations(self, observations: list[Observation]) -> None:
        self._executemany("INSERT INTO observations VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE total_consumer_fare=VALUES(total_consumer_fare), extraction_status=VALUES(extraction_status)", [(item.observation_id, item.period, item.route, item.origin, item.destination, item.booking_window_days, item.total_consumer_fare, item.source_id, item.carrier, item.fare_class, item.observation_date, item.is_duplicate, item.raw_fare, item.collection_timestamp, item.extraction_status, item.stops, item.source_url) for item in observations])

    def save_validation_issues(self, issues: list[dict[str, str]]) -> None:
        self._executemany("INSERT INTO validation_issues (observation_id, issue_type, detail, created_at) VALUES (%s,%s,%s,%s)", [(issue["observation_id"], issue["issue_type"], issue["detail"], datetime.now(timezone.utc).isoformat()) for issue in issues])

    def save_weights(self, weights: Weights) -> None:
        rows = [("route_weight", key, value) for key, value in weights.route_weights.items()]
        rows += [("window_weight", str(key), value) for key, value in weights.window_weights.items()]
        if weights.airfare_weight is not None:
            rows.append(("airfare_weight", "airfare", weights.airfare_weight))
        self._executemany("INSERT INTO weights VALUES (%s,%s,%s) ON DUPLICATE KEY UPDATE value=VALUES(value)", rows)
        metadata = [("route_weight", key, value.source, value.status, value.reference) for key, value in weights.route_weight_metadata.items()]
        metadata += [("window_weight", str(key), value.source, value.status, value.reference) for key, value in weights.window_weight_metadata.items()]
        if weights.airfare_weight_metadata:
            value = weights.airfare_weight_metadata
            metadata.append(("airfare_weight", "airfare", value.source, value.status, value.reference))
        self._executemany("INSERT INTO weight_metadata VALUES (%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE source=VALUES(source), status=VALUES(status), reference=VALUES(reference)", metadata)

    def load_observations(self) -> list[Observation]:
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM observations ORDER BY observation_id")
        rows = cursor.fetchall()
        cursor.close()
        return [Observation(**row) for row in rows]

    def load_weights(self) -> Weights:
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM weights")
        rows = cursor.fetchall()
        cursor.execute("SELECT * FROM weight_metadata")
        metadata = cursor.fetchall()
        cursor.close()
        routes = {row["weight_key"]: float(row["value"]) for row in rows if row["weight_type"] == "route_weight"}
        windows = {int(row["weight_key"]): float(row["value"]) for row in rows if row["weight_type"] == "window_weight"}
        airfare = next((float(row["value"]) for row in rows if row["weight_type"] == "airfare_weight"), None)
        route_metadata = {row["weight_key"]: WeightMetadata(row["source"], row["status"], row["reference"]) for row in metadata if row["weight_type"] == "route_weight"}
        airfare_row = next((row for row in metadata if row["weight_type"] == "airfare_weight"), None)
        airfare_metadata = WeightMetadata(airfare_row["source"], airfare_row["status"], airfare_row["reference"]) if airfare_row else None
        return Weights(routes, windows, airfare, route_metadata, {}, airfare_metadata)

    def save_report(self, report: dict, base_period: str = "base", current_period: str = "current") -> int:
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO reports (generated_at, base_period, current_period, report_json) VALUES (%s,%s,%s,%s)", (datetime.now(timezone.utc).isoformat(), base_period, current_period, json.dumps(report)))
        self.connection.commit()
        report_id = cursor.lastrowid
        cursor.close()
        return int(report_id)

    def close(self) -> None:
        self.connection.close()


def create_mysql_repositories(host: str = "127.0.0.1", port: int = 3306, user: str = "root", password: str | None = None) -> tuple[MySQLRepository, MySQLRepository]:
    """Open the separate scrape and output databases."""
    return MySQLRepository("airfare_source", host, port, user, password), MySQLRepository("airfare_results", host, port, user, password)