from pydantic import Field
from fastapi_users import models
from fastapi_users.db import TortoiseBaseUserModel
from tortoise.contrib.pydantic import PydanticModel

from .models import User as UserModel
from .models import Role


class User(models.BaseUser):
    username: str
    phone_number: str
    role: Role = Field(alias='role_id')


class UserCreate(models.BaseUserCreate):
    username: str
    phone_number: str
    role: Role = Field(alias='role_id')


class UserUpdate(models.BaseUserUpdate):
    username: str
    phone_number: str
    role: Role = Field(alias='role_id')


class UserDB(User, models.BaseUserDB, PydanticModel):
    class Config:
        orm_mode = True
        orig_model = UserModel
