import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

from intelligence.data import load_cpi_airfare_weight, load_weights
from intelligence.index_engine.apix import calculate_apix_report
from intelligence.models import Observation, Weights
from intelligence.storage import IntelligenceRepository


class AirfareService:
    """Service orchestrating access to Intelligence repositories and API responses."""

    def __init__(
        self,
        source_db_path: str | Path = "data/source.db",
        result_db_path: str | Path = "data/results.db",
    ) -> None:
        self.source_db_path = Path(source_db_path)
        self.result_db_path = Path(result_db_path)

    def _get_source_repo(self) -> IntelligenceRepository:
        return IntelligenceRepository(self.source_db_path)

    def _get_result_repo(self) -> IntelligenceRepository:
        return IntelligenceRepository(self.result_db_path)

    def get_latest_report(self) -> Dict[str, Any]:
        """Fetch the most recent report from results.db or calculate from source.db."""
        if self.result_db_path.exists():
            try:
                conn = sqlite3.connect(self.result_db_path)
                conn.row_factory = sqlite3.Row
                row = conn.execute(
                    "SELECT report_json, generated_at FROM reports ORDER BY report_id DESC LIMIT 1"
                ).fetchone()
                conn.close()
                if row:
                    report = json.loads(row["report_json"])
                    report["generated_at"] = row["generated_at"]
                    return report
            except Exception:
                pass

        # Fallback: compute dynamically from source.db if present
        if self.source_db_path.exists():
            try:
                source_repo = self._get_source_repo()
                obs = source_repo.load_observations()
                weights = source_repo.load_weights()
                source_repo.close()
                if obs and weights and weights.route_weights:
                    return calculate_apix_report(obs, weights)
            except Exception:
                pass

        # Return default BLOCKED report if no data exists
        return {
            "apix": None,
            "base": 100.0,
            "index_name": "Airfare Price Index",
            "calculation_status": "BLOCKED",
            "reason": "NO_COLLECTION_DATA",
            "weighting_status": "MISSING_INPUT",
            "methodology": "CPI 2024 / Jevons elementary indices aggregated with authoritative route weights",
            "airfare_weight": None,
            "airfare_weight_metadata": None,
            "route_components": [],
            "booking_window_components": [],
            "components": [],
            "validation_issues": [
                {
                    "issue_type": "no_collection_data",
                    "detail": "No live observation records or calculation reports were found in the database.",
                }
            ],
            "confidence": {"score": 0.0, "components": {}},
            "insights": [],
        }

    def get_summary(self) -> Dict[str, Any]:
        report = self.get_latest_report()
        apix = report.get("apix")
        base = report.get("base", 100.0)
        
        index_change = (apix - base) if (apix is not None and base) else None
        index_change_percentage = ((apix - base) / base * 100) if (apix is not None and base) else None

        # Fetch observation statistics from source DB
        raw_count = 0
        clean_count = 0
        last_timestamp = report.get("generated_at")
        active_routes_count = len(report.get("route_components", []))
        
        if self.source_db_path.exists():
            try:
                conn = sqlite3.connect(self.source_db_path)
                conn.row_factory = sqlite3.Row
                r_row = conn.execute("SELECT COUNT(*) as cnt FROM raw_observations").fetchone()
                c_row = conn.execute("SELECT COUNT(*) as cnt FROM observations").fetchone()
                t_row = conn.execute("SELECT collection_timestamp FROM raw_observations ORDER BY collection_timestamp DESC LIMIT 1").fetchone()
                conn.close()
                if r_row:
                    raw_count = r_row["cnt"]
                if c_row:
                    clean_count = c_row["cnt"]
                if t_row and t_row["collection_timestamp"]:
                    last_timestamp = t_row["collection_timestamp"]
            except Exception:
                pass

        confidence = report.get("confidence", {})
        components = confidence.get("components", {}) if isinstance(confidence, dict) else {}

        return {
            "apix": apix,
            "base": base,
            "index_change": index_change,
            "index_change_percentage": index_change_percentage,
            "calculation_status": report.get("calculation_status", "BLOCKED"),
            "reason": report.get("reason"),
            "weighting_status": report.get("weighting_status", "MISSING_INPUT"),
            "source_coverage": {
                "active_sources": 2,
                "confidence_score": components.get("source_coverage", 0.0),
            },
            "route_coverage": {
                "active_routes": active_routes_count,
                "confidence_score": components.get("route_coverage", 0.0),
            },
            "observation_counts": {
                "raw_total": raw_count,
                "clean_total": clean_count,
                "components_total": len(report.get("components", [])),
            },
            "last_collection_timestamp": last_timestamp,
            "cpi_airfare_weight": report.get("airfare_weight"),
            "weight_provenance": report.get("airfare_weight_metadata"),
        }

    def get_routes(self) -> List[Dict[str, Any]]:
        report = self.get_latest_report()
        route_components = report.get("route_components", [])
        if route_components:
            return route_components
        
        components = report.get("components", [])
        routes_dict: Dict[str, Dict[str, Any]] = {}
        for comp in components:
            route = comp.get("route")
            if not route:
                continue
            if route not in routes_dict:
                routes_dict[route] = {
                    "route": route,
                    "route_weight": comp.get("route_weight", 0.0),
                    "elementary_index": comp.get("elementary_index", 0.0),
                    "route_elementary_index": comp.get("route_elementary_index", 0.0),
                    "base_representative_fare": comp.get("base_representative_fare"),
                    "current_representative_fare": comp.get("current_representative_fare"),
                    "comparable_observations": comp.get("comparable_observations", 0),
                }
        return list(routes_dict.values())

    def get_observations(self, limit: int = 100, period: Optional[str] = None) -> List[Dict[str, Any]]:
        if not self.source_db_path.exists():
            return []
        try:
            repo = self._get_source_repo()
            obs = repo.load_observations()
            repo.close()
            if period:
                obs = [o for o in obs if o.period.lower() == period.lower()]
            result = []
            for item in obs[:limit]:
                d = item.__dict__.copy()
                result.append(d)
            return result
        except Exception:
            return []

    def get_quality(self) -> Dict[str, Any]:
        report = self.get_latest_report()
        confidence = report.get("confidence", {})
        return {
            "score": confidence.get("score", 0.0) if isinstance(confidence, dict) else 0.0,
            "components": confidence.get("components", {}) if isinstance(confidence, dict) else {},
            "validation_issues": report.get("validation_issues", []),
        }

    def get_status(self) -> Dict[str, Any]:
        summary = self.get_summary()
        return {
            "calculation_status": summary["calculation_status"],
            "reason": summary.get("reason"),
            "weighting_status": summary["weighting_status"],
            "last_collection_timestamp": summary["last_collection_timestamp"],
            "raw_observations": summary["observation_counts"]["raw_total"],
            "clean_observations": summary["observation_counts"]["clean_total"],
            "source_db_exists": self.source_db_path.exists(),
            "result_db_exists": self.result_db_path.exists(),
        }

    def get_metadata(self) -> Dict[str, Any]:
        report = self.get_latest_report()
        return {
            "index_name": report.get("index_name", "Airfare Price Index"),
            "methodology": report.get("methodology", "CPI 2024 / Jevons elementary indices aggregated with authoritative route weights"),
            "cpi_airfare_weight": report.get("airfare_weight"),
            "cpi_airfare_metadata": report.get("airfare_weight_metadata"),
            "base": report.get("base", 100.0),
        }

    def recalculate_report(self) -> Dict[str, Any]:
        if not self.source_db_path.exists():
            return self.get_latest_report()
        source_repo = self._get_source_repo()
        result_repo = self._get_result_repo()
        obs = source_repo.load_observations()
        weights = source_repo.load_weights()
        try:
            report = calculate_apix_report(obs, weights)
        except Exception as e:
            report = {
                "apix": None,
                "base": 100.0,
                "index_name": "Airfare Price Index",
                "calculation_status": "BLOCKED",
                "reason": "MISSING_GENUINE_BASE_PERIOD",
                "weighting_status": "MISSING_INPUT",
                "methodology": "CPI 2024 / Jevons elementary indices aggregated with authoritative route weights",
                "airfare_weight": getattr(weights, "airfare_weight", None),
                "airfare_weight_metadata": getattr(weights, "airfare_weight_metadata", None),
                "route_components": [],
                "booking_window_components": [],
                "components": [],
                "validation_issues": [{"issue_type": "missing_genuine_base_period", "detail": str(e)}],
                "confidence": {"score": 0.0, "components": {}},
                "insights": [],
            }
        result_repo.save_report(report)
        source_repo.close()
        result_repo.close()
        return report

