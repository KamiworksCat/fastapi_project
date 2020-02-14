from fastapi.encoders import jsonable_encoder

from app import crud
from app.database import db_session
from app.schema.user import UserCreate
from app.tests.utils.general import random_lower_string


def test_user_crud():
    email = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create(db_session, obj_in=user_in)
    assert user.email == email
    assert hasattr(user, "hashed_password")
    is_administrator = crud.user.is_administrator(user)
    assert is_administrator is False

    # Authenticate user
    # Test should pass since the user is in the database
    authenticated_user = crud.user.authenticate(
        db_session, email=email, password=password
    )
    assert authenticated_user
    assert user.email == authenticated_user.email

    # Test creating administrator
    email = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password, is_administrator=True)
    user = crud.user.create(db_session, obj_in=user_in)
    is_administrator = crud.user.is_administrator(user)
    assert is_administrator is True


def test_not_authenticate_user():
    email = random_lower_string()
    password = random_lower_string()
    user = crud.user.authenticate(db_session, email=email, password=password)
    assert user is None


def test_get_user():
    password = random_lower_string()
    username = random_lower_string()
    user_in = UserCreate(email=username, password=password, is_superuser=True)
    user = crud.user.create(db_session, obj_in=user_in)
    user_2 = crud.user.get(db_session, obj_id=user.id)
    assert user.email == user_2.email
    assert jsonable_encoder(user) == jsonable_encoder(user_2)
