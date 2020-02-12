import logging

from app import config, crud
from app.schema.user import UserCreate
from database.base_class import Base
from database.db import engine, db_session


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db(db_session):
    Base.metadata.create_all(engine)
    user = crud.user.get_by_email(db_session, email=config.FIRST_SUPERUSER)
    if not user:
        user_in = UserCreate(
            email=config.FIRST_SUPERUSER,
            password=config.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        crud.user.create(db_session, obj_in=user_in)


def init():
    init_db(db_session)


def main():
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
