from fastapi import FastAPI
from starlette.testclient import TestClient

from app import main, config, crud
from app.database import db_session
from app.schema.user import UserCreate

client = TestClient(main.app)


def test_get_access_token():
    login_data = {
        "username": config.FIRST_SUPERUSER,
        "password": config.FIRST_SUPERUSER_PASSWORD,
    }
    user_in = UserCreate(email=login_data["username"], password=login_data["password"])
    crud.user.create(db_session, obj_in=user_in)
    response = client.post(f"{config.API_PREFIX}/login/token", data=login_data)
    tokens = response.json()
    assert "access_token" in tokens
    assert tokens["access_token"]
    assert response.status_code == 200
