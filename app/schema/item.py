from pydantic import BaseModel


class ItemBase(BaseModel):
    identifier: str = None
    title: str = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class ItemUpdate(ItemBase):
    pass
