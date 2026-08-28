import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Ensure backend path is in sys.path
backend_path = Path(__file__).resolve().parent.parent / "backend"
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "service" in data


def test_airfare_summary_endpoint():
    response = client.get("/api/v1/airfare/summary")
    assert response.status_code == 200
    data = response.json()
    assert "calculation_status" in data
    assert "weighting_status" in data
    assert "observation_counts" in data


def test_airfare_index_endpoint():
    response = client.get("/api/v1/airfare/index")
    assert response.status_code == 200
    data = response.json()
    assert "calculation_status" in data
    assert "methodology" in data


def test_airfare_routes_endpoint():
    response = client.get("/api/v1/airfare/routes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_airfare_observations_endpoint():
    response = client.get("/api/v1/airfare/observations?limit=10")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_airfare_quality_endpoint():
    response = client.get("/api/v1/airfare/quality")
    assert response.status_code == 200
    data = response.json()
    assert "score" in data
    assert "validation_issues" in data


def test_airfare_status_endpoint():
    response = client.get("/api/v1/airfare/status")
    assert response.status_code == 200
    data = response.json()
    assert "calculation_status" in data
    assert "weighting_status" in data


def test_airfare_metadata_endpoint():
    response = client.get("/api/v1/airfare/metadata")
    assert response.status_code == 200
    data = response.json()
    assert "index_name" in data
    assert "methodology" in data
