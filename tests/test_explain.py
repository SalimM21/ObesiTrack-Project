import pytest
from fastapi.testclient import TestClient

import api


client = TestClient(api.app)

@pytest.fixture(autouse=True)
def mock_shap(monkeypatch):
    class DummyExplainer:
        def shap_values(self, X):
            return [[0.1, -0.2, 0.3]]

    monkeypatch.setattr("obesitrack.explainability.GLOBAL_EXPLAINER", DummyExplainer())
    yield

def test_explain_shap_success(auth_headers):
    payload = {"Age": 25, "FCVC": 3, "NCP": 2, "CH2O": 2, "FAF": 1}
    resp = client.post("/explain/shap", json=payload, headers=auth_headers)
    assert resp.status_code == 200
    body = resp.json()
    assert "shap_values" in body
    assert isinstance(body["shap_values"], list)
