from fastapi.params import Depends
from tortoise.exceptions import DoesNotExist

from apps.common.managers import TortoiseDatabase

from apps.telegram.managers import TelegramManager
from apps.telegram.schemas import TelegramDB, BodyTelegramReferralLink
from apps.telegram.models import Telegram, TelegramReferralLink


def get_telegram_db():
    yield TortoiseDatabase(TelegramDB, Telegram)


def get_telegram_manager(telegram_db: TortoiseDatabase = Depends(get_telegram_db)):
    yield TelegramManager(telegram_db)


async def get_telegram_or_referral_link(
        user,
        telegram_manager
) -> TelegramDB | BodyTelegramReferralLink:
    try:
        return await telegram_manager.get(user_id=user.id)
    except DoesNotExist:
        referral_link = await TelegramReferralLink.get_or_create(user_id=user.id)
        return BodyTelegramReferralLink(link=referral_link[0].code)
