from database import db_session, engine
from fastapi import FastAPI
from inital_data import init_db
from routers import user, item, auth
from models_schemas.users import User
from models_schemas.items import Item

from constants import error_responses

User.metadata.create_all(bind=engine)
Item.metadata.create_all(bind=engine)
app = FastAPI(title="FastAPI Sample Project")


@app.get("/")
async def read_main():
    init_db(db_session)
    return {"msg": "Hello World"}


app.include_router(router=auth.router,
                   tags=["login"],
                   responses=error_responses("User"))
app.include_router(router=user.router,
                   prefix="/users",
                   tags=["users"],
                   responses=error_responses("User"))
app.include_router(router=item.router,
                   prefix="/items",
                   tags=["items"],
                   responses=error_responses("Item"))
