from typing import Optional
from dataclasses import dataclass

from aiogram import types

from apps.telegram.models import Telegram
from apps.users.models import User


@dataclass()
class TelegramInfo:
    id: int
    username: str
    first_name: str
    last_name: str


class UserData:

    def __init__(self, obj: types.Message):
        self.telegram_info = TelegramInfo(
           id=obj.chat.id,
           username=obj.chat.username,
           first_name=obj.chat.first_name,
           last_name=obj.chat.last_name,
        )
        self.user: Optional[User] = None

    @property
    def is_created(self) -> bool:
        return self.user is not None

    async def setup(self):
        self.user = await User.filter(telegram__chat_id=self.telegram_info.id).first()
        return self
