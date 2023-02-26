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
