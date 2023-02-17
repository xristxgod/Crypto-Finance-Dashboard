from fastapi_users.db import TortoiseUserDatabase

from .schemas import UserDB
from .models import User


def get_user_db():
    yield TortoiseUserDatabase(UserDB, User)
