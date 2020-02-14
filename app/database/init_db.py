from app import config, crud
from app.schema.user import UserCreate
from app.database import base


def init_db(db_session):
    user = crud.user.get_by_email(db_session, email=config.FIRST_SUPERUSER)
    if not user:
        user_in = UserCreate(
            email=config.FIRST_SUPERUSER,
            password=config.FIRST_SUPERUSER_PASSWORD,
            is_administrator=True,
        )
        crud.user.create(db_session, obj_in=user_in)
