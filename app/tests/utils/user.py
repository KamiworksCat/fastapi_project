from app import crud
from app.database import db_session
from app.schema.user import UserCreate
from app.tests.utils import random_lower_string


def create_random_user():
    email = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(username=email, email=email, password=password)
    user = crud.user.create(db_session=db_session, obj_in=user_in)
    return user
