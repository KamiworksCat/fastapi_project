from fastapi import APIRouter

from constants import error_responses
from routers import auth, user, item

api_router = APIRouter()

api_router.include_router(router=auth.router,
                          tags=["login"],
                          responses=error_responses("User"))
api_router.include_router(router=user.router,
                          prefix="/users",
                          tags=["users"],
                          responses=error_responses("User"))
api_router.include_router(router=item.router,
                          prefix="/items",
                          tags=["items"],
                          responses=error_responses("Item"))
