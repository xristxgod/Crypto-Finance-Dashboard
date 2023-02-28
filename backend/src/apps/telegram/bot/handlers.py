from aiogram import types

from apps.telegram.bot import services
from apps.telegram.bot.middlewares.user_database import BaseUser, AnonymousUser
from apps.telegram.bot.utils import current_user
from apps.telegram.bot.messanger import messanger


async def start(message: types.Message, user: BaseUser):
    referral_code = None
    if ' ' in message.text:
        referral_code = message.text.split()[1]

    if isinstance(user, AnonymousUser) and referral_code is None:
        return await messanger.get_message('user_not_found', user, message)

    if user.is_created:
        return await messanger.get_message('menu', user, message)
    else:
        if await services.registration_by_referral_link(code=referral_code, user=user):
            return await messanger.get_message('success_registration', user, message)
        else:
            return await messanger.get_message('referral_code_not_found', user, message)


@current_user
async def menu(message: types.Message, user: BaseUser):
    return await messanger.get_message('menu', user, message)
