from __future__ import absolute_import

from .common import *
from .tests import *

if NETWORK == 'DEV':
    from .dev import *


__all__ = (
    'Settings',
)


class Settings:
    ROOT_DIR = ROOT_DIR
    LOGGING_CONFIG_FILE = LOGGING_CONFIG_FILE

    TITLE: str = TITLE
    VERSION: str = VERSION
    APPS_MODELS: tuple = APPS_MODELS

    NETWORK: str = NETWORK
    DATABASE_CONFIG: dict = DATABASE_CONFIG
    TEST_DATABASE_CONFIG: dict = TEST_DATABASE_CONFIG

    SECRET_KEY_AUTH: str = SECRET_KEY_AUTH

    TELEGRAM_TOKEN: str = TELEGRAM_TOKEN
    TELEGRAM_BOT_NAME: str = TELEGRAM_BOT_NAME

    WEBHOOK_URL = WEBHOOK_URL
    COOKIE_NAME: str = COOKIE_NAME
