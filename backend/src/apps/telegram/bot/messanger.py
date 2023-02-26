from tortoise import transactions
from fastapi_cache.decorator import cache

from apps.telegram.models import Message
from apps.telegram.bot.services import UserData

__all__ = (
    'messanger',
)

EXPIRE_TIME = 60


class messanger:

    tags = (
        'user_not_found',
        'start',
    )

    @classmethod
    async def setup(cls):
        async with transactions.in_transaction('default'):
            message = Message.filter(tag__in=cls.tags)
            if await message.count() != cls.tags:
                database_tags = set(await message.values_list('tag', flat=True))
                await Message.exclude(tag__in=cls.tags).delete()
                await Message.bulk_create([
                    Message(tag=tag)
                    for tag in set(cls.tags).difference(database_tags)
                ])

    @classmethod
    async def _make_message(cls, message: dict, user: UserData):
        from aiogram import types

        if message['message']:
            pass

    @classmethod
    @cache(expire=EXPIRE_TIME)
    async def get_message(cls, tag: str, user: UserData):
        message = await Message.get_message(tag, user.language_id)
        return await cls._make_message(message, user)
