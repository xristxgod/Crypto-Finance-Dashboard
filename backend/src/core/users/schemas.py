from typing import Optional

from pydantic import BaseModel, EmailStr
from fastapi_users import schemas


class _AbstractBodyUser(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    language_id: Optional[str] = 'ENG'


class BodyUser(schemas.BaseUser, _AbstractBodyUser):
    pass


class BodyCreateUser(schemas.BaseUserCreate, _AbstractBodyUser):
    pass


class BodyUpdateUser(schemas.BaseUserUpdate, _AbstractBodyUser):
    pass
