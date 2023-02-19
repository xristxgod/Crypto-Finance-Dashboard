from aiogram import Bot, Dispatcher, types

from config import settings


bot_app = Bot(token=settings.TELEGRAM_TOKEN)
dp = Dispatcher(bot_app)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer(f"Salom")
