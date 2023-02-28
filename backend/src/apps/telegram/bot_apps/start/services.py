from typing import Optional

from aiogram import types
from tortoise import transactions

from apps.telegram.models import Telegram, TelegramReferralLink
from apps.telegram.middlewares.tg_user_database import BaseUser


async def get_referral_code(message: types.Message) -> Optional[str]:
    return message.text.split()[1] if ' ' in message.text else None


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
