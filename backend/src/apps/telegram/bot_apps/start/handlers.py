from aiogram import types

from apps.telegram.middlewares.tg_user_database import BaseUser, AnonymousUser
from apps.telegram.utils import tg_current_user as current_user
from apps.telegram.tg_messanger import tg_messanger as messanger

from . import services


async def start_handler(message: types.Message, user: BaseUser):
    referral_code = await services.get_referral_code(message.text)

    if isinstance(user, AnonymousUser) and referral_code is None:
        return await messanger.get_message('user_not_found', user, message)

    if user.is_created:
        return await messanger.get_message('menu', user, message)
    else:
        if await services.registration_by_referral_link(code=referral_code, user=user):
            return await messanger.get_message('success_registration', user, message)
        else:
            return await messanger.get_message('referral_code_not_found', user, message)


async def registration_handler(value: types.CallbackQuery | types.Message, user: BaseUser, **kwargs):
    pass


@current_user
async def menu_handler(message: types.Message, user: BaseUser):
    return await messanger.get_message('menu', user, message)
