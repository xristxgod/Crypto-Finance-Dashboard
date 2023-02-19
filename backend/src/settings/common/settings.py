from __future__ import absolute_import

import os
from pathlib import Path

NETWORK = os.getenv('NETWORK', 'DEV')

ROOT_DIR = Path(__file__).parent.parent.parent.parent

APPS_MODELS = (
    'apps.users.models',
    'apps.telegram.models',
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
        'crypto_dashboard': {
            'models': APPS_MODELS,
        }
    },
    'timezone': 'UTC'
}

TITLE = rf'Crypto dashboard: Binance\ByBit | {NETWORK}'
VERSION = '0.0.1'

SECRET_KEY_AUTH = os.getenv('SECRET_KEY_AUTH')

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

WEBHOOK_URL = os.getenv('WEBHOOK_URL')
