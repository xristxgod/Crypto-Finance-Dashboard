from datetime import datetime

from pydantic import BaseModel
from tortoise.contrib.pydantic.base import PydanticModel

from core.users import BodySubModel
from apps.telegram.models import Telegram


class ResponseTelegramReferralLink(BaseModel):
    link: str


class BodyTelegram(BodySubModel, PydanticModel):
    chat_id: int
    username: str
    is_active: bool
    created_at: datetime
    modified_at: datetime

    class Config:
        orm_mode = True
        model = Telegram
        exclude = (
            'user',
        )
