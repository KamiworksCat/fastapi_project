from typing import List

from pydantic import BaseModel

from app.schema.item import Item


class UserBase(BaseModel):
    """
    If quota is 0, user is allowed unlimited items
    """
    name: str = None
    email: str = None
    is_administrator: bool = False
    quota: int = 0


class UserBaseInDB(UserBase):
    id: int = None

    class Config:
        orm_mode = True


class UserInDb(UserBaseInDB):
    hashed_password: str
    disabled: bool = False


class UserCreate(UserBaseInDB):
    email: str
    password: str


class UserUpdate(UserBaseInDB):
    password: str = None


class User(UserBaseInDB):
    items: List[Item] = []
