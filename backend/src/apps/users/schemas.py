from typing import Optional

from pydantic import EmailStr
from fastapi_users import models
from tortoise.contrib.pydantic import PydanticModel

from apps.users.models import User


class BodyUser(models.BaseUser):
    username: str
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None


class BodyUserCreate(models.BaseUserCreate):
    username: str
    phone_number: Optional[str]
    email: Optional[EmailStr] = None


class BodyUserUpdate(models.BaseUserUpdate):
    username: str
    phone_number: str
    email: Optional[EmailStr] = None


class UserDB(BodyUser, models.BaseUserDB, PydanticModel):

    class Config:
        orm_mode = True
        orig_model = User
