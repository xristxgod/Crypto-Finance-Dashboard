from __future__ import absolute_import

from .common import *

if os.getenv('NETWORK', 'DEV'):
    from .dev import *

from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = DATABASE_URL
    DATABASE_INDEXES_NAMING_CONVENTION: dict = DATABASE_INDEXES_NAMING_CONVENTION
    SECRET_AUTH: str = SECRET_AUTH
