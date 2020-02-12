from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

from app import config
from app.database import db_session, SessionLocal
from app.inital_data import init_db
from routers.api_router import api_router

app = FastAPI(title="FastAPI Sample Project")


@app.get("/")
async def read_main():
    init_db(db_session)
    return {"msg": "Hello World"}


app.include_router(api_router, prefix=config.API_PREFIX)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response
