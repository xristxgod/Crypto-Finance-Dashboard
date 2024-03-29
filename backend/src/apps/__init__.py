from fastapi import APIRouter

from .telegram import routers as tg_router

router = APIRouter()

# Telegram
router.include_router(tg_router.telegram_router, prefix='/telegram', tags=['Telegram'])
# Telegram bot_apps
router.include_router(tg_router.telegram_bot_router, prefix='/telegram-bot_apps', tags=['Telegram Bot'])
