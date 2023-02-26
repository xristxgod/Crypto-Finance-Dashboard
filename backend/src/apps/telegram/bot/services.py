import functools
from typing import Optional, Callable
from dataclasses import dataclass

from tortoise import transactions

from core.users.models import User
from apps.telegram.models import Telegram, TelegramReferralLink


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


def current_user(func: Callable):
    @functools.wraps(func)
    async def wrapper(message, user: BaseUser, **kwargs):
        if isinstance(user, AnonymousUser):
            from apps.telegram.bot.messanger import messanger
            return messanger.get_message('user_not_found', user, message)
        return await func(message, user, **kwargs)
    return wrapper


async def registration_by_referral_link(code: str, user: BaseUser) -> bool:
    async with transactions.in_transaction('default'):
        referral = await TelegramReferralLink.get(code=code)
        if not referral:
            return False
        await Telegram.create(
            id=user.telegram_info.id,
            username=user.telegram_info.username,
            user=referral.user_id
        )
        return True
