from __future__ import absolute_import

import os
from settings.common import APPS_MODELS


TEST_DATABASE_CONFIG = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.asyncpg',
            'credentials': {
                'host': os.getenv('DATABASE_HOST'),
                'port': int(os.getenv('DATABASE_PORT', '5432')),
                'user': os.getenv('DATABASE_USER'),
                'password': os.getenv('DATABASE_PASSWORD'),
                'database': os.getenv('TEST_DATABASE_NAME'),
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
