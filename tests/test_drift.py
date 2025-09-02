# tests/test_drift.py
import pytest
from fastapi.testclient import TestClient
from obesitrack.main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_drift(monkeypatch):
    def dummy_report():
        return {
            "status": "ok",
            "drift_detected": False,
            "metrics": {"kolmogorov_smirnov": 0.05}
        }
    monkeypatch.setattr("obesitrack.drift.get_drift_report", dummy_report)
    yield

def test_drift_report(auth_headers):
    resp = client.get("/drift/report", headers=auth_headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert "metrics" in body
    assert "kolmogorov_smirnov" in body["metrics"]
