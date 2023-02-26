from aiogram import types
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from apps.telegram.bot import services


class UserMiddleware(LifetimeControllerMiddleware):
    async def pre_process(self, obj: types.Message, data, *args):
        if hasattr(obj, "update_id"):
            data['user'] = None
        else:
            data['user'] = await services.Manager.setup(obj)

    async def post_process(self, obj, data, *args):
        if 'user' in data.keys():
            del data["user"]
