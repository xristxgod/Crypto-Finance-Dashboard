from __future__ import absolute_import

import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent.parent

DATABASE_URL = os.getenv('DATABASE_URL')

SECRET_AUTH = os.getenv("SECRET_AUTH")

DATABASE_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}