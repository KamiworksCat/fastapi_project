from datetime import timedelta

from sqlalchemy.orm import Session

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from app.schema.auth import Token
from app import crud
from app.utils import create_access_token
from starlette.status import HTTP_401_UNAUTHORIZED

from app.database import get_db

router = APIRouter()


@router.post("/login/token", response_model=Token, summary="Login user for access token", tags=["login"])
async def login_for_access_token(db: Session = Depends(get_db),
                                 form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.user.authenticate(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    elif crud.user.is_disabled(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"email": user.email, "user_id": user.id},
                                       expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
