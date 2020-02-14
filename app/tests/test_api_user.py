from app import crud, config
from app.database.db import db_session
from app.schema.user import UserCreate
from app.tests.utils.general import random_lower_string, test_client

user_api = f"{config.API_PREFIX}/users"
client = test_client


def test_get_users_superuser_me(superuser_token_headers):
    response = client.get(f"{user_api}/me", headers=superuser_token_headers)
    current_user = response.json()
    print(current_user)
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_administrator"]
    assert current_user["email"] == config.FIRST_SUPERUSER


def test_get_users_normal_user_me(normal_user_token_headers):
    response = client.get(f"{user_api}/me", headers=normal_user_token_headers)
    current_user = response.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_administrator"] is False
    assert current_user["email"] == config.EMAIL_TEST_USER


def test_create_user_new_email(superuser_token_headers):
    username = random_lower_string()
    password = random_lower_string()
    data = {"email": username, "password": password}
    response = client.post(f"{user_api}/users/",
                           headers=superuser_token_headers, json=data)
    created_user = response.json()
    user = crud.user.get_by_email(db_session, email=username)
    print(created_user)
    assert user.email == created_user["email"]
    assert 200 <= response.status_code < 300


def test_get_existing_user(superuser_token_headers):
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.user.create(db_session, obj_in=user_in)
    user_id = user.id
    response = client.get(f"{user_api}/{user_id}", headers=superuser_token_headers)
    api_user = response.json()
    user = crud.user.get_by_email(db_session, email=username)
    assert user.email == api_user["email"]
    assert 200 <= response.status_code < 300


def test_create_user_existing_username(superuser_token_headers):
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    crud.user.create(db_session, obj_in=user_in)
    data = {"email": username, "password": password}
    response = client.post(f"{config.API_PREFIX}/users/",
                           headers=superuser_token_headers, json=data)
    created_user = response.json()
    print(created_user)
    assert "_id" not in created_user
    assert response.status_code == 400


def test_create_user_by_normal_user(normal_user_token_headers):
    username = random_lower_string()
    password = random_lower_string()
    data = {"email": username, "password": password}
    response = client.post(f"{config.API_PREFIX}/users/",
                           headers=normal_user_token_headers, json=data)
    assert response.status_code == 400


def test_retrieve_users(superuser_token_headers):
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    crud.user.create(db_session, obj_in=user_in)

    username2 = random_lower_string()
    password2 = random_lower_string()
    user_in2 = UserCreate(email=username2, password=password2)
    crud.user.create(db_session, obj_in=user_in2)

    response = client.get(f"{config.API_PREFIX}/users/", headers=superuser_token_headers)
    all_users = response.json()

    assert len(all_users) > 1
    for user in all_users:
        assert "email" in user
