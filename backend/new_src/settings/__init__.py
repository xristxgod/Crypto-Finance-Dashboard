from __future__ import absolute_import

from .common import *
from .tests import *

if NETWORK == 'DEV':
    from .dev import *


__all__ = (
    'Settings',
)


class Settings:
    NETWORK: str = NETWORK
    # Dirs
    ROOT_DIR = ROOT_DIR
    LOGGING_CONFIG_FILE = LOGGING_CONFIG_FILE
    # Swagger
    TITLE: str = TITLE
    VERSION: str = VERSION
    # Database
    APPS_MODELS: tuple = APPS_MODELS
    DATABASE_CONFIG: dict = DATABASE_CONFIG
    TEST_DATABASE_CONFIG: dict = TEST_DATABASE_CONFIG
    # Auth
    COOKIE_NAME: str = COOKIE_NAME
    AUTH_SECRET_KEY: str = AUTH_SECRET_KEY
    # Telegram
    TELEGRAM_BOT_CONFIG: dict = TELEGRAM_BOT_CONFIG
    # Other
    WEBHOOK_URL = WEBHOOK_URL
