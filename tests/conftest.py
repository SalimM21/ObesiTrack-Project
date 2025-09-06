import pytest
from fastapi.testclient import TestClient

import api


client = TestClient(api.app)

@pytest.fixture
def auth_headers():
    # Suppose qu’on a déjà un user seedé en DB pour les tests
    resp = client.post("/auth/token", data={"username": "test", "password": "test"})
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
