import pytest
from app.config import settings
from jose import jwt
from main import app
from fastapi.testclient import TestClient
client2 = TestClient(app)

global header_access_token, header_refresh_token


# @pytest.mark.skip
@pytest.mark.asyncio
def test_register(client, create):
    response = client2.post(
        "/auth/register",
        json={
            "password_confirm": "stringst",
            "password": "stringst",
            "email": "user@example.com",
            "born": "2025-01-30",
            "name": "string137"})
    assert response.status_code == 200
    assert "id" in response.json()
    assert "name" in response.json()
    assert "email" in response.json()
    assert "role_id" in response.json()


# @pytest.mark.skip
@pytest.mark.asyncio
def test_login(client, create):
    headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
    response = client.post(
        "/auth/login/",
        data={"username": settings.DEFAULT_USERNAME, "password": settings.DEFAULT_PASSWORD.get_secret_value()},
        headers=headers)
    user_id = 1
    global header_access_token, header_refresh_token
    header_access_token = response.json().get("access_token")
    header_refresh_token = response.json().get("refresh_token")
    cookie_access_token = response.cookies.get("access_token")
    cookie_refresh_token = response.cookies.get("refresh_token")

    id_from_access = jwt.decode(
            header_access_token,
            settings.JWT_SECRET_KEY.get_secret_value(),
            algorithms=[settings.JWT_ALGORITHM])
    id_from_refresh = jwt.decode(
            header_refresh_token,
            settings.JWT_SECRET_KEY.get_secret_value(),
            algorithms=[settings.JWT_ALGORITHM])

    assert response.status_code == 200
    assert header_access_token == cookie_access_token
    assert header_refresh_token == cookie_refresh_token
    assert id_from_access.get("sub") == str(user_id)
    assert id_from_refresh.get("sub") == str(user_id)


# @pytest.mark.skip
@pytest.mark.asyncio
def test_logout(client, create):
    global header_access_token, header_refresh_token
    cookies = {
        'access_token': header_access_token,
        'refresh_token': header_refresh_token,
    }
    response = client.post("/auth/logout/", cookies=cookies)
    assert response.status_code == 200




