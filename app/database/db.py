from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from starlette.requests import Request

from app.config import SQLALCHEMY_DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db(request: Request):
    return request.state.db
