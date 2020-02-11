from datetime import timedelta

from config import ACCESS_TOKEN_EXPIRE_MINUTES
from database import db_session
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from models_schemas.auth_schemas import Token
from utils import authenticate_user, create_access_token
from starlette.status import HTTP_401_UNAUTHORIZED

router = APIRouter()


@router.post("/login/token", response_model=Token, summary="Login user for access token", tags=["login"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db_session, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
