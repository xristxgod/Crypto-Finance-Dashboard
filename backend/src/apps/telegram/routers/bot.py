from fastapi import APIRouter
from fastapi.requests import Request
from aiogram import Dispatcher, Bot, types

from apps.telegram.bot.messanger import messanger
from apps.telegram.bot import bot, dp
from apps.telegram.config import TELEGRAM_WEBHOOK_URL

router = APIRouter()


@router.on_event('startup')
async def startup():
    # Create messanger
    await messanger.setup()
    # Create webhook
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != TELEGRAM_WEBHOOK_URL:
        await bot.set_webhook(
            url=TELEGRAM_WEBHOOK_URL
        )


@router.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()


@router.post('')
async def bot_webhook(request: Request):
    telegram_update = types.Update(**await request.json())
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(telegram_update)
