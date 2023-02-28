from tortoise import transactions

from apps.telegram.models import Telegram, TelegramReferralLink
from apps.telegram.bot.middlewares.user_database import BaseUser


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
