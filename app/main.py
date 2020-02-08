from fastapi import FastAPI

from app.database import SessionLocal

app = FastAPI()


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}
