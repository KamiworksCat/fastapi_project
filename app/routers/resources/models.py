import uuid

from pydantic import BaseModel, UUID4

from app.routers.users.models import User


class Resource(BaseModel):
    user: User
    identifier: UUID4 = uuid.uuid4()
