import requests

from app import crud, config
from app.database.db import db_session
from app.schema.user import UserCreate
from app.tests.utils import get_server_api, random_lower_string

user_api = f"{get_server_api()}{config.API_PREFIX}/users"


def test_get_users_superuser_me(superuser_token_headers):
    response = requests.get(f"{user_api}/me", headers=superuser_token_headers)
    current_user = response.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_administrator"]
    assert current_user["email"] == config.FIRST_SUPERUSER


def test_get_users_normal_user_me(normal_user_token_headers):
    response = requests.get(f"{user_api}/me", headers=normal_user_token_headers)
    current_user = response.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_administrator"] is False
    assert current_user["email"] == config.EMAIL_TEST_USER


def test_create_user_new_email(superuser_token_headers):
    username = random_lower_string()
    password = random_lower_string()
    data = {"email": username, "password": password}
    response = requests.post(f"{user_api}/users/",
                             headers=superuser_token_headers, json=data)
    assert 200 <= response.status_code < 300
    created_user = response.json()
    user = crud.user.get_by_email(db_session, email=username)
    assert user.email == created_user["email"]


def test_get_existing_user(superuser_token_headers):
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.user.create(db_session, obj_in=user_in)
    user_id = user.id
    response = requests.get(
        f"{user_api}/{user_id}",
        headers=superuser_token_headers,
    )
    assert 200 <= response.status_code < 300
    api_user = response.json()
    user = crud.user.get_by_email(db_session, email=username)
    assert user.email == api_user["email"]


def test_create_user_existing_username(superuser_token_headers):
    server_api = get_server_api()
    username = random_lower_string()
    # username = email
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    crud.user.create(db_session, obj_in=user_in)
    data = {"email": username, "password": password}
    response = requests.post(
        f"{server_api}{config.API_PREFIX}/users/",
        headers=superuser_token_headers,
        json=data,
    )
    created_user = response.json()
    assert response.status_code == 400
    assert "_id" not in created_user


def test_create_user_by_normal_user(normal_user_token_headers):
    server_api = get_server_api()
    username = random_lower_string()
    password = random_lower_string()
    data = {"email": username, "password": password}
    response = requests.post(
        f"{server_api}{config.API_PREFIX}/users/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400


def test_retrieve_users(superuser_token_headers):
    server_api = get_server_api()
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    crud.user.create(db_session, obj_in=user_in)

    username2 = random_lower_string()
    password2 = random_lower_string()
    user_in2 = UserCreate(email=username2, password=password2)
    crud.user.create(db_session, obj_in=user_in2)

    response = requests.get(
        f"{server_api}{config.API_PREFIX}/users/", headers=superuser_token_headers
    )
    all_users = response.json()

    assert len(all_users) > 1
    for user in all_users:
        assert "email" in user
