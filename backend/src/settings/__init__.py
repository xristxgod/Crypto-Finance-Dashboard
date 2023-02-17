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

    NETWORK: str = NETWORK
    ROOT_DIR = ROOT_DIR
    DATABASE_CONFIG: dict = DATABASE_CONFIG
