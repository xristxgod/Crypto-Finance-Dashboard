from aiogram import Dispatcher


def registration_handlers(dp: Dispatcher):
    from . import handlers
    dp.register_message_handler(handlers.start_handler, commands=['start'])
