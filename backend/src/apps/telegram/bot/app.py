from aiogram import Bot, Dispatcher

from config import settings
from apps.telegram.bot import middlewares
from apps.telegram.bot import handlers

__all__ = (
    'app',
    'dp',
)


app = Bot(token=settings.TELEGRAM_BOT_CONFIG['token'])
dp = Dispatcher(app)

dp.middleware.setup(middlewares.UserDatabaseMiddleware())

dp.register_message_handler(handlers.start, commands=['start'])
