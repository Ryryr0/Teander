from datetime import datetime, timezone, timedelta

import jwt
import uvicorn
from fastapi.testclient import TestClient

from database.database import async_engine, Base
from main import app
from config import settings
import asyncio


client = TestClient(app)


def test_reg():
    response_reg = client.post(
        "/users/reg",
        data={
            "username": "test_user_1",
            "email": "testuser1@gmail.com",
            "password": "test_user_1",
        }
    )
    assert response_reg.status_code == 201


def test_token():
    response_token = client.post(
        "/users/token",
        data={
            "grant_type": "password",
            "username": "user_test_1",
            "password": "user_test_1",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        }
    )
    assert response_token.status_code == 200


def test_update():
    response_token = client.post(
        "/users/token",
        data={
            "grant_type": "password",
            "username": "user_test_1",
            "password": "user_test_1",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        }
    )

    assert response_token.status_code == 200
    token = response_token.json()

    response_update = client.put(
        "/users/update-user",
        headers={
            "Authorization:": f"{token["token_type"]} {token["access_token"]}",
        },
        data={
            "username": "user_test_1_update",
            "email": "user_test_1",
        }
    )
    assert response_update.status_code == 200


def test_delete():
    response_token = client.post(
        "/users/token",
        data={
            "grant_type": "password",
            "username": "user_test_1_update",
            "password": "user_test_1",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        }
    )
    assert response_token.status_code == 200
    token = response_token.json()

    response_delete = client.post(
        "/users/delete",
        headers={
            "Authorization:": f"{token["token_type"]} {token["access_token"]}",
        },
    )
    assert response_delete.status_code == 200

    response_token = client.post(
        "/users/token",
        data={
            "grant_type": "password",
            "username": "user_test_1_update",
            "password": "user_test_1",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        }
    )
    assert response_token.status_code == 401
