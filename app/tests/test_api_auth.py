import requests
from fastapi import FastAPI
from starlette.testclient import TestClient

from app import config


app = FastAPI()
client = TestClient(app)


def test_get_access_token():
    login_data = {
        "username": config.FIRST_SUPERUSER,
        "password": config.FIRST_SUPERUSER_PASSWORD,
    }
    response = client.post("/login/token", data=login_data)
    tokens = response.json()
    print(tokens)
    print(response)
    assert "access_token" in tokens
    assert tokens["access_token"]
    assert response.status_code == 200
