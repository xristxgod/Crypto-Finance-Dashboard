from aiogram import Bot, Dispatcher

from config import settings
from . import middlewares
from . import handlers

__all__ = (
    'app',
    'dp',
)


app = Bot(token=settings.TELEGRAM_TOKEN)
dp = Dispatcher(app)

dp.middleware.setup(middlewares.UserMiddleware())

dp.register_message_handler(handlers.start, commands=['start'])
