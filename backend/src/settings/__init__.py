from __future__ import absolute_import

from .common import *

if NETWORK == 'DEV':
    from .dev import *


__all__ = (
    'Settings',
)


class Settings:
    TITLE: str = TITLE
    VERSION: str = VERSION
    APPS_MODELS: tuple = APPS_MODELS

    NETWORK: str = NETWORK
    ROOT_DIR = ROOT_DIR
    DATABASE_CONFIG: dict = DATABASE_CONFIG

    SECRET_KEY_AUTH: str = SECRET_KEY_AUTH

    TELEGRAM_TOKEN: str = TELEGRAM_TOKEN
    TELEGRAM_BOT_NAME: str = TELEGRAM_BOT_NAME

    WEBHOOK_URL = WEBHOOK_URL
