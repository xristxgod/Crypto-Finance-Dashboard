from tortoise import transactions
from apps.telegram.middlewares.tg_user_database import BaseUser

from core.users.schemas import BodyUser
from core.users.managers import UserManager, SubModelNotExits
from apps.telegram.models import Telegram, TelegramReferralLink
from apps.telegram.schemas import ResponseTelegramReferralLink


async def get_telegram(
        user: BodyUser,
        telegram_manager: UserManager
) -> Telegram | ResponseTelegramReferralLink:
    try:
        return await telegram_manager.get_sub_model(user_id=user.id)
    except SubModelNotExits:
        link, _ = await TelegramReferralLink.get_or_create(user_id=user.id)
        return ResponseTelegramReferralLink(link=link.url)


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
