from app import crud, config
from app.database import db_session
from app.schema.user import UserCreate
from app.tests.utils.general import random_lower_string


def create_random_user():
    email = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(username=email, email=email, password=password)
    user = crud.user.create(db_session=db_session, obj_in=user_in)
    return user


def user_authentication_headers(email, password):
    from app.tests.utils.general import test_client
    data = {"username": email, "password": password}

    response = test_client.post(f"{config.API_PREFIX}/login/token", data=data)
    response_data = response.json()
    auth_token = response_data["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers
