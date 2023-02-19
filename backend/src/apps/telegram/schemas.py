from pydantic import BaseModel, validator
from tortoise.contrib.pydantic import PydanticModel

from .models import Telegram


class BodyTelegram(BaseModel):
    chat_id: int
    username: str
    is_active: bool

    @validator('username')
    def username_validator(cls, v: str):
        if not v.startswith('@'):
            v = '@' + v
        return v


class TelegramDB(BodyTelegram, PydanticModel):
    class Config:
        orm_mode = True
        orig_model = Telegram
