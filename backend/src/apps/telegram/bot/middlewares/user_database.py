from typing import Optional
from dataclasses import dataclass

from aiogram import types
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from core.users.models import User


@dataclass()
class TelegramInfo:
    id: int
    username: str
    first_name: str
    last_name: str


class BaseUser:
    def __init__(self, telegram_info: TelegramInfo, language_id: Optional[str] = 'ENG'):
        self.telegram_info = telegram_info
        self.language_id = language_id

    @property
    def chat_id(self) -> int:
        return self.telegram_info.id

    @property
    def username(self) -> str:
        return self.telegram_info.username

    @property
    def is_created(self) -> bool:
        return False


class CurrentUser(BaseUser):

    def __init__(self, user: User, telegram_info: TelegramInfo):
        self.info = user
        super().__init__(telegram_info=telegram_info, language_id=user.language_id)

    @property
    def is_created(self) -> bool:
        return True


class AnonymousUser(BaseUser):
    pass


class Manager:

    @classmethod
    async def setup(cls, obj) -> BaseUser:
        telegram_info = TelegramInfo(
            id=obj.chat.id,
            username='@' + obj.chat.username,
            first_name=obj.chat.first_name,
            last_name=obj.chat.last_name,
        )
        user = await User.get_or_none(telegram__id=telegram_info.id)
        if user:
            return CurrentUser(user=user, telegram_info=telegram_info)
        return AnonymousUser(telegram_info=telegram_info)


class Middleware(LifetimeControllerMiddleware):
    async def pre_process(self, obj: types.Message, data, *args):
        if hasattr(obj, "update_id"):
            data['user'] = None
        else:
            data['user'] = await Manager.setup(obj)

    async def post_process(self, obj, data, *args):
        if 'user' in data.keys():
            del data["user"]
