from __future__ import absolute_import

import os
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent.parent

APPS_MODELS = (
    '',
)

DATABASE_CONFIG = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.asyncpg',
            'credentials': {
                'host': os.getenv('DATABASE_HOST'),
                'port': os.getenv('DATABASE_PORT'),
                'user': os.getenv('DATABASE_USER'),
                'password': os.getenv('DATABASE_PASSWORD'),
                'database': os.getenv('DATABASE_NAME'),
            }
        },
    },
    'apps': {
        'my_app': {
            'models': APPS_MODELS,
            'default_connection': 'default',
        }
    },
    'timezone': 'UTC'
}
