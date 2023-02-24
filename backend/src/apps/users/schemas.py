from typing import Optional

from pydantic import EmailStr, UUID4
from fastapi_users import models
from tortoise.contrib.pydantic import PydanticModel

from apps.users.models import User


class BodyUser(models.UserProtocol):
    id: UUID4
    username: str
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None


class BodyUserCreate(Base):
    username: str
    phone_number: Optional[str]
    email: Optional[EmailStr] = None


class BodyUserUpdate(models.BaseUserUpdate):
    username: str
    phone_number: Optional[str]
    email: Optional[EmailStr]


class UserDB(BodyUser, models.BaseUserDB, PydanticModel):

    class Config:
        orm_mode = True
        orig_model = User
