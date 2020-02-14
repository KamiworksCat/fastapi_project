import random
import string

from starlette.testclient import TestClient

from app import config, main, crud


test_client = TestClient(main.app)


def random_lower_string():
    return "".join(random.choices(string.ascii_lowercase, k=32))


def get_superuser_token_headers():
    from app.tests.utils.user import user_authentication_headers
    from app.database import db_session
    user = crud.user.get_by_email(db_session=db_session, email=config.FIRST_SUPERUSER)
    if not user:
        from schema.user import UserCreate
        user_obj = UserCreate(email=config.FIRST_SUPERUSER, password=config.FIRST_SUPERUSER_PASSWORD,
                              is_administrator=True)
        crud.user.create(db_session=db_session, obj_in=user_obj)
    login_data = {
        "username": config.FIRST_SUPERUSER,
        "password": config.FIRST_SUPERUSER_PASSWORD,
    }
    return user_authentication_headers(email=login_data["username"],
                                       password=login_data["password"])
