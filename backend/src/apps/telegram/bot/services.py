from typing import Optional, NoReturn, Self
from dataclasses import dataclass

from aiogram import types
from tortoise import transactions, exceptions

from apps.telegram.models import Telegram, TelegramReferralLink
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
           username='@' + obj.chat.username,
           first_name=obj.chat.first_name,
           last_name=obj.chat.last_name,
        )
        self.user: Optional[User] = None

    @property
    def chat_id(self) -> int:
        return self.telegram_info.id

    @property
    def username(self) -> str:
        return self.telegram_info.username

    @property
    def is_created(self) -> bool:
        return self.user is not None

    async def add_to_db(self, user: User) -> NoReturn:
        async with transactions.atomic():
            telegram = Telegram(
                chat_id=self.chat_id,
                username=self.username,
                user=user,
            )
            self.user = user
            await TelegramReferralLink.filter(user=user).delete()
            await telegram.save()

    async def setup(self) -> Self:
        self.user = await User.filter(telegram__chat_id=self.telegram_info.id).first()
        return self
