import config
import crud
from models_schemas.users.schemas import UserCreate


def init_db(db_session):
    user = crud.user.get_by_email(db_session, email=config.FIRST_SUPERUSER)
    if not user:
        user_in = UserCreate(
            email=config.FIRST_SUPERUSER,
            password=config.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        crud.user.create(db_session, user=user_in)
