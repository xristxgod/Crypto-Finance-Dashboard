from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, UUID4
from tortoise.contrib.pydantic import PydanticModel

from .credential_manager import Keys
from .models import Service
from .models import Account


class BodyService(BaseModel):
    id: str
    credential_manager_cls_name: str


class BodyAccount(BaseModel):
    id: UUID4
    name: str
    service: str
    created_at: datetime
    modified_at: datetime


class BodyAccountDetail(BodyAccount):
    keys: Optional[Keys] = Field(default_factory=dict)


class BodyCreateAccount(BaseModel):
    name: str
    keys: Optional[Keys] = Field(default_factory=dict)


class AccountDB(BodyAccount, PydanticModel):
    class Config:
        orm_mode = True
        orig_model = Account


class ServiceDB(BodyService, PydanticModel):
    class Config:
        orm_mode = True
        orig_model = Service
