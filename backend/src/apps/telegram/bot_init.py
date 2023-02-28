from aiogram import Bot, Dispatcher

from config import settings
from apps.telegram import middlewares
from apps.telegram import bot_apps

__all__ = (
    'app',
    'dp',
)


app = Bot(token=settings.TELEGRAM_BOT_CONFIG['token'])
dp = Dispatcher(app)

dp.middleware.setup(middlewares.TGUserDatabaseMiddleware())

# Registration bot apps
bot_apps.registration(dp)
