from fastapi import APIRouter
from fastapi.requests import Request
from aiogram import Dispatcher, Bot, types

from apps.telegram.bot.app import app, dp
from apps.telegram.config import TELEGRAM_WEBHOOK_URL


router = APIRouter()


@router.on_event("startup")
async def on_startup():
    webhook_info = await app.get_webhook_info()
    if webhook_info.url != TELEGRAM_WEBHOOK_URL:
        await app.set_webhook(
            url=TELEGRAM_WEBHOOK_URL
        )


@router.post('')
async def bot_webhook(request: Request):
    telegram_update = types.Update(**await request.json())
    Dispatcher.set_current(dp)
    Bot.set_current(app)
    await dp.process_update(telegram_update)


@router.on_event("shutdown")
async def on_shutdown():
    await app.session.close()
