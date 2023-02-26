from __future__ import absolute_import

import os
from pathlib import Path

NETWORK = os.getenv('NETWORK', 'DEV')

ROOT_DIR = Path(__file__).parent.parent.parent
CONFIG_DIR = ROOT_DIR / 'config'
LOGGING_CONFIG_FILE = CONFIG_DIR / 'logging.ini'

APPS_MODELS = (
    # Core
    'core.users.models',
    # Apps
    'apps.telegram.models',
    # 'apps.accounts.models',
)

DATABASE_CONFIG = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.asyncpg',
            'credentials': {
                'host': os.getenv('DATABASE_HOST'),
                'port': int(os.getenv('DATABASE_PORT', '5432')),
                'user': os.getenv('DATABASE_USER'),
                'password': os.getenv('DATABASE_PASSWORD'),
                'database': os.getenv('DATABASE_NAME'),
            }
        },
    },
    'apps': {
        'default': {
            'models': APPS_MODELS,
        }
    },
    'timezone': 'UTC'
}

REDIS_URL = os.getenv('REDIS_URL')

LANGUAGES = (
    'ENG',
    'RU',
)

TITLE = rf'Crypto dashboard: Binance\ByBit | {NETWORK}'
VERSION = '0.0.1'

COOKIE_NAME = 'AUTH_TOKEN'
AUTH_SECRET_KEY = os.getenv('AUTH_SECRET_KEY')

TELEGRAM_BOT_CONFIG = {
    'name': os.getenv('TELEGRAM_BOT_NAME'),
    'token': os.getenv('TELEGRAM_TOKEN')
}

WEBHOOK_URL = os.getenv('WEBHOOK_URL')
