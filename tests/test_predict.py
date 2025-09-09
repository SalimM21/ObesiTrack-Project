import pytest
from httpx import AsyncClient
from fastapi import status
from app.main import app
from app.db.models import Prediction


@pytest.mark.asyncio
async def test_make_prediction_success(async_session, test_user, token_headers, monkeypatch):
    # Mock du service predictor
    def fake_predict(data: dict):
        return "positive", {"positive": 0.9, "negative": 0.1}

    monkeypatch.setattr("app.services.predictor.predict", fake_predict)

    payload = {
        "age": 35,
        "glucose": 120.0,
        "bmi": 28.0,
        "bloodpressure": 80.0,
        "pedigree": 0.5,
        "sex": "male",
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/predictions/predict", json=payload, headers=token_headers)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "result" in data
    assert "probability" in data
    assert data["result"] == "positive"
    assert isinstance(data["probability"], dict)


@pytest.mark.asyncio
async def test_make_prediction_unauthorized(async_session):
    payload = {
        "age": 40,
        "glucose": 110.0,
        "bmi": 26.0,
        "bloodpressure": 78.0,
        "pedigree": 0.4,
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/predictions/predict", json=payload)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_my_history_empty(async_session, test_user, token_headers):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/predictions/me", headers=token_headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.asyncio
async def test_my_history_with_predictions(async_session, test_user, token_headers):
    # Pré-remplir une prédiction
    pred = Prediction(
        user_id=test_user.id,
        input_json={"age": 25, "glucose": 100, "bmi": 22.5, "bloodpressure": 75, "pedigree": 0.2},
        predicted_label="negative",
        probabilities={"negative": 0.85, "positive": 0.15},
    )
    async_session.add(pred)
    await async_session.commit()

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/predictions/me", headers=token_headers)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["predicted_label"] == "negative"
