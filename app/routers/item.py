import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.database.db import get_db
from app.utils import get_current_active_user
from app.models.user import User as DBUser
from app.schema.item import Item, ItemCreate, ItemUpdate

router = APIRouter()


@router.get("/", response_model=List[Item])
def read_items(db: Session = Depends(get_db), skip: int = 0,
               limit: int = 100, current_user: DBUser = Depends(get_current_active_user)):
    """
    Retrieve items.
    """
    if crud.user.is_administrator(current_user):
        items = crud.item.get_multi(db, skip=skip, limit=limit)
    else:
        items = crud.item.get_multi_by_owner(db_session=db, owner_id=current_user.id, skip=skip, limit=limit)
    return items


@router.post("/", response_model=Item)
def create_item(*, db: Session = Depends(get_db),
                item_in: ItemCreate, current_user: DBUser = Depends(get_current_active_user)):
    """
    Create new item.
    """
    # Check if user quota is filled before creating the item
    if current_user.quota != 0 and len(current_user.items) >= current_user.quota:
        raise HTTPException(status_code=403, detail="You have already reached the max quota")
    item_in.identifier = str(uuid.uuid4())
    item = crud.item.create_with_owner(db_session=db, obj_in=item_in, owner_id=current_user.id)
    return item


@router.put("/{item_id}", response_model=Item)
def update_item(*, db: Session = Depends(get_db), item_id: int,
                item_in: ItemUpdate, current_user: DBUser = Depends(get_current_active_user)):
    """
    Update an item.
    """
    item = crud.item.get(db_session=db, obj_id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not crud.user.is_administrator(current_user) and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    item_in.identifier = str(uuid.uuid4())
    item = crud.item.update(db_session=db, db_obj=item, obj_in=item_in)
    return item


@router.get("/{item_id}", response_model=Item)
def read_item(*, db: Session = Depends(get_db), item_id: int,
              current_user: DBUser = Depends(get_current_active_user)):
    """
    Get item by ID.
    """
    item = crud.item.get(db_session=db, obj_id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not crud.user.is_administrator(current_user) and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return item


@router.delete("/{item_id}", response_model=List[Item])
def delete_item(*, db: Session = Depends(get_db), item_id: int,
                current_user: DBUser = Depends(get_current_active_user)):
    """
    Delete an item.
    """
    item = crud.item.get(db_session=db, obj_id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not crud.user.is_administrator(current_user) and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    crud.item.remove(db_session=db, obj_id=item_id)
    items = crud.item.get_multi_by_owner(db, owner_id=current_user.id)
    return items
