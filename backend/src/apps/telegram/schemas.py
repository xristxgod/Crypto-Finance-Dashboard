from pydantic import BaseModel, validator
from tortoise.contrib.pydantic import PydanticModel

from apps.common.managers import BaseModelDB
from apps.telegram.models import Telegram


class BodyTelegram(BaseModel):
    chat_id: int
    username: str
    is_active: bool

    @validator('username')
    def username_validator(cls, v: str):
        if not v.startswith('@'):
            v = '@' + v
        return v


class BodyTelegramReferralLink(BaseModel):
    link: str


class TelegramDB(BodyTelegram, BaseModelDB, PydanticModel):
    class Config:
        orm_mode = True
        orig_model = Telegram
