from aiogram import types
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from .services import UserData


class UserMiddleware(LifetimeControllerMiddleware):
    async def pre_process(self, obj: types.Message, data, *args):
        if hasattr(obj, "update_id"):
            data['user'] = None
        else:
            data['user'] = await UserData(obj).setup()

    async def post_process(self, obj, data, *args):
        if 'user' in data.keys():
            del data["user"]
