from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, UUID4
from tortoise.contrib.pydantic import PydanticModel

from .credential_manager import Keys
from .models import Service
from .models import Account


class BodyAccount(BaseModel):
    id: UUID4
    name: str
    service: str
    created_at: datetime
    modified_at: datetime


class BodyAccountDetail(BodyAccount):
    keys: Optional[Keys] = Field(default_factory=dict)


class AccountDB(BodyAccount, PydanticModel):

    class Config:
        orm_mode = True
        orig_model = Account

    def with_keys(self) -> BodyAccountDetail:
        pass
