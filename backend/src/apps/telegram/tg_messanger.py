import re
import json
from typing import Any

import emoji
from aiogram import types
from tortoise import transactions
from fastapi_cache.decorator import cache

from config import settings
from apps.telegram.models import Message
from apps.telegram.middlewares.tg_user_database import BaseUser
from apps.telegram.config import TELEGRAM_CONFIG_DIR

__all__ = (
    'tg_messanger',
)

EXPIRE_TIME = 60


class tg_messanger:
    args_pattern = re.compile(r'(?P<args>{{[A-Z]+}})')

    tags = (
        'start',
        'referral_code_not_found',
        'user_not_found',
        'success_registration',
        'menu',
    )

    @classmethod
    async def __set_default_message(cls, messages: list[Message]):
        import aiofiles
        async with transactions.in_transaction('default'):
            async with aiofiles.open(TELEGRAM_CONFIG_DIR / 'default_en_messages.json') as file:
                default_messages = json.loads(await file.read())

            update_message = []
            for message in messages:
                valid_default_message = list(filter(lambda x: x['tag'] == message.tag, default_messages))
                if valid_default_message:
                    setattr(message, 'message_ENG', json.dumps(valid_default_message[0].get('message_ENG')))
                    update_message.append(message)

            if update_message:
                await Message.bulk_update(update_message, fields=['message_ENG'])

    @classmethod
    async def setup(cls, set_default_message: bool = False):
        async with transactions.in_transaction('default'):
            message = Message.filter(tag__in=cls.tags)
            if await message.count() != cls.tags:
                database_tags = set(await message.values_list('tag', flat=True))
                await Message.exclude(tag__in=cls.tags).delete()
                messages = await Message.bulk_create([
                    Message(tag=tag)
                    for tag in set(cls.tags).difference(database_tags)
                ])
                if set_default_message:
                    await cls.__set_default_message(messages)

    @classmethod
    async def _make_text(cls, text: str):
        for raw_arg in re.findall(cls.args_pattern, text):
            arg = raw_arg.replace('{{', '').replace('}}', '')
            text = text.replace(raw_arg, str(getattr(settings, arg)))

        return emoji.emojize(text, language='alias')

    @classmethod
    async def _make_message(cls, db_message: dict[str, Any], user: BaseUser,
                            message: types.Message | types.CallbackQuery):
        from apps.telegram.bot_init import app as bot

        message_conf = {
            'chat_id': user.chat_id,
            'text': await cls._make_text(db_message.get('text', 'Error'))
        }

        if db_message.get('inline_button'):
            keyboard = types.InlineKeyboardMarkup()
            for button in db_message['inline_button']:
                if button.get('text'):
                    button['text'] = await cls._make_text(button['text'])
                keyboard.add(types.InlineKeyboardButton(**button))
            message_conf['reply_markup'] = keyboard

        return await bot.send_message(**message_conf)

    @classmethod
    @cache(expire=EXPIRE_TIME)
    async def get_message(cls, tag: str, user: BaseUser, message: types.Message | types.CallbackQuery):
        db_message = await Message.get_message(tag, user.language_id)
        return await cls._make_message(db_message, user, message)
