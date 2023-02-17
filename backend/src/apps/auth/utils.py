from fastapi_users.db import TortoiseUserDatabase

from apps.auth.schemas import UserDB
from apps.users.models import User


def get_user_db():
    yield TortoiseUserDatabase(UserDB, User)
