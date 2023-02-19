from aiogram import types

from .app import dp
from .services import UserData
from apps.telegram.models import TelegramReferralLink


@dp.message_handler(commands=['start'])
async def start(message: types.Message, user: UserData):
    if user.is_created:
        pass

    referral_code = None
    if " " in message.text:
        referral_code = message.text.split()[1]

        referral_code = await TelegramReferralLink.get(code=referral_code)

        if referral_code.exists():
            await user.add_to_db(referral_code.user)

