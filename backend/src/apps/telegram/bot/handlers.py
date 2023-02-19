from aiogram import types

from .app import dp
from .services import UserData


@dp.message_handler(commands=['start'])
async def start(message: types.Message, user: UserData):
    if user.is_created:
        pass
    else:
        pass
