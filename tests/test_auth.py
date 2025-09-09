# tests/test_auth.py

import pytest
from httpx import AsyncClient
from fastapi import status
from app.main import app
from app.db.models import User


@pytest.mark.asyncio
async def test_signup_success(async_session, monkeypatch):
    # Mock hash_password et create_access_token
    monkeypatch.setattr("app.core.security.hash_password", lambda pwd: "hashed_" + pwd)
    monkeypatch.setattr("app.core.security.create_access_token", lambda **kwargs: "fake_token")

    payload = {"email": "newuser@example.com", "password": "strongpass", "full_name": "Test User"}

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/signup", json=payload)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["access_token"] == "fake_token"


@pytest.mark.asyncio
async def test_signup_existing_email(async_session, test_user):
    payload = {"email": test_user.email, "password": "anypass", "full_name": "Existing"}

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/signup", json=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Email déjà enregistré"


@pytest.mark.asyncio
async def test_login_success(async_session, test_user, monkeypatch):
    monkeypatch.setattr("app.core.security.verify_password", lambda plain, hashed: True)
    monkeypatch.setattr("app.core.security.create_access_token", lambda **kwargs: "fake_token_login")

    payload = {"email": test_user.email, "password": "correctpass", "full_name": "Ignored"}

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/login", json=payload)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["access_token"] == "fake_token_login"


@pytest.mark.asyncio
async def test_login_invalid_credentials(async_session, test_user, monkeypatch):
    monkeypatch.setattr("app.core.security.verify_password", lambda plain, hashed: False)

    payload = {"email": test_user.email, "password": "wrongpass", "full_name": "Ignored"}

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/login", json=payload)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Identifiants incorrects"
