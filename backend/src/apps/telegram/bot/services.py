from typing import Optional, NoReturn, Self
from dataclasses import dataclass

from aiogram import types
from tortoise import transactions

from core.users.models import User
from apps.telegram.models import Telegram


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
            username='@' + obj.chat.username,
            first_name=obj.chat.first_name,
            last_name=obj.chat.last_name,
        )
        self.info: Optional[User] = None
        self.language_id = 'ENG'

    @property
    def chat_id(self) -> int:
        return self.telegram_info.id

    @property
    def username(self) -> str:
        return self.telegram_info.username

    @property
    def is_created(self) -> bool:
        return self.info is not None

    async def add_to_db(self, user: User) -> NoReturn:
        async with transactions.in_transaction('default'):
            await Telegram.create(
                chat_id=self.chat_id,
                username=self.username,
                user=user,
            )
            self.info = user
            self.language_id = user.language.id

    async def setup(self) -> Self:
        self.info = await User.filter(telegram__chat_id=self.telegram_info.id).first()
        return self
