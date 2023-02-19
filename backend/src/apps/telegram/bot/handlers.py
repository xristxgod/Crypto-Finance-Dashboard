from aiogram import types

from .services import UserData
from apps.telegram.models import TelegramReferralLink


async def start(message: types.Message, user: UserData):
    if user is None:
        return

    if user.is_created:
        pass
    else:
        referral_code = None
        if " " in message.text:
            referral_code = await TelegramReferralLink.get(code=message.text.split()[1])

            if referral_code.exists():
                await user.add_to_db(await referral_code.user.first())
