from aiogram import types

from apps.telegram.bot import services
from apps.telegram.models import TelegramReferralLink
from apps.telegram.bot.messanger import messanger


async def start(message: types.Message, user: services.UserData):
    if user is None:
        return await messanger.get_message()

    if user.is_created:
        pass
    else:
        referral_code = None
        if " " in message.text:
            referral_code = await TelegramReferralLink.get(code=message.text.split()[1])

            if referral_code.exists():
                await user.add_to_db(await referral_code.user.first())
