from pydantic import Field
from fastapi_users import models
from tortoise.contrib.pydantic import PydanticModel

from apps.users.models import User
from apps.users.models import Role


class BodyUser(models.BaseUser):
    username: str
    phone_number: str
    role: Role = Field(alias='role_id')


class BodyUserCreate(models.BaseUserCreate):
    username: str
    phone_number: str
    role: Role = Field(alias='role_id')


class BodyUserUpdate(models.BaseUserUpdate):
    username: str
    phone_number: str
    role: Role = Field(alias='role_id')


class UserDB(BodyUser, models.BaseUserDB, PydanticModel):
    class Config:
        orm_mode = True
        orig_model = User
