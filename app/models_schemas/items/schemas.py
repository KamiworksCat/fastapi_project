import uuid

from pydantic import BaseModel, UUID4


class ItemBase(BaseModel):
    identifier: UUID4 = uuid.uuid4()


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_int: int

    class Config:
        orm_mode = True


class ItemUpdate(ItemBase):
    pass
