from typing import List

from pydantic import BaseModel

from models_schemas.items.schemas import Item


class UserBase(BaseModel):
    """
    If quota is 0, user is allowed unlimited items
    """
    name: str = None
    is_administrator: bool = False
    disabled: bool = False
    email: str = None
    quota: int = 0


class UserBaseInDB(UserBase):
    id: int = None

    class Config:
        orm_mode = True


class UserInDb(UserBaseInDB):
    hashed_password: str


class UserCreate(UserBaseInDB):
    email: str
    password: str


class UserUpdate(UserBaseInDB):
    password: str = None


class User(UserBaseInDB):
    id: int
    items: List[Item] = []
