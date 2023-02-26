from aiogram import types
from tortoise import transactions
from fastapi_cache.decorator import cache

from apps.telegram.models import Message
from apps.telegram.bot.services import BaseUser

__all__ = (
    'messanger',
)

EXPIRE_TIME = 60


class messanger:

    tags = (
        'referral_code_not_found',
        'user_not_found',
        'start',
        'menu',
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
    async def _make_message(cls, db_message: dict, user: BaseUser, message: types.Message):
        from apps.telegram.bot import bot

        message_conf = {
            'chat_id': user.chat_id,
            'text': db_message.get('message', ' ')
        }

        if db_message.get('inline_button'):
            keyboard = types.InlineKeyboardMarkup()
            for button in db_message['inline_button']:
                keyboard.add(**button)
            message_conf['reply_markup'] = keyboard

        return await bot.send_message(**message_conf)

    @classmethod
    @cache(expire=EXPIRE_TIME)
    async def get_message(cls, tag: str, user: BaseUser, message: types.Message):
        db_message = await Message.get_message(tag, user.language_id)
        return await cls._make_message(db_message, user, message)
