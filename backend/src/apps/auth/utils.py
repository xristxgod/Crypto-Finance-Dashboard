from fastapi_users.db import TortoiseUserDatabase

from .schemas import UserDB
from apps.users.models import User

__all__ = (
    'get_user_db',
)


def get_user_db():
    yield TortoiseUserDatabase(UserDB, User)
