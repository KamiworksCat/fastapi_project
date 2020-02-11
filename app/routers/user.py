from typing import List

from fastapi import Depends, HTTPException, APIRouter, Body
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from sqlalchemy.orm import Session

import crud
from database import get_db
from models_schemas.users import models, schemas
from utils import get_current_active_user

router = APIRouter()


@router.get("/me", response_model=schemas.User, summary="Read current user")
async def read_users_me(current_user: models.User = Depends(get_current_active_user)):
    return current_user


@router.post("/", response_model=schemas.User, summary="Create a user")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_active_user)):
    """
    Create user with all of the information below:
     - **name**: Non unique instance
     - **email**: Email must be unique
     - **password**: Password will be hashed before the user is saved
     - **quota**: To determine the number of items that the user can have/generate

    * The user using this api must be an administrator or api will throw permission denied exception
    """
    if not current_user.is_administrator:
        raise HTTPException(status_code=403, detail="User does not have the right to perform this action")
    db_user = crud.user.get_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.user.create_user(db=db, user=user)


@router.get("/", response_model=List[schemas.User], summary="Get list of active users")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
               user: models.User = Depends(get_current_active_user)):
    """
    If user is not administrator, this api will only return current user
    """
    if user.is_administrator:
        users = crud.user.get_multi(db, skip=skip, limit=limit)
    else:
        users = get_current_active_user()
    return users


@router.get("/{user_id}", response_model=schemas.User, summary="Read specific user")
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.user.get(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/{user_id}", response_model=schemas.User, summary="Delete specific user")
def delete_user(user_id: int, db: Session = Depends(get_db),
                user: models.User = Depends(get_current_active_user)):
    if not user.is_administrator:
        raise HTTPException(status_code=403, detail="User cannot perform this action")
    db_user = crud.user.get(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    crud.user.remove(db_session=db, obj_id=user_id)
    return "User has been removed from the system"


@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(get_current_active_user),
):
    """
    Update a user.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    elif user != current_user or not current_user.is_administrator:
        raise HTTPException(status_code=403, detail="You may only update your own profile")
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user
