from aiogram import Bot, Dispatcher, types

from config import settings
from . import middlewares

__all__ = (
    'app',
    'dp',
)


app = Bot(token=settings.TELEGRAM_TOKEN)
dp = Dispatcher(app)

dp.middleware.setup(middlewares.UserMiddleware())
