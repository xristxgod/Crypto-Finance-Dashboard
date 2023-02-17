from typing import Optional

from fastapi.params import Depends
from fastapi.requests import Request
from fastapi_users.manager import BaseUserManager
from fastapi_users.db import TortoiseUserDatabase

from config import settings
from apps.users.schemas import BodyUserCreate, UserDB
from .utils import get_user_db

__all__ = (
    'UserManager',
    'get_user_manager',
)


class UserManager(BaseUserManager[BodyUserCreate, UserDB]):
    user_db_model = UserDB
    reset_password_token_secret = settings.SECRET_KEY_AUTH
    verification_token_secret = settings.SECRET_KEY_AUTH

    async def on_after_register(self, user: UserDB, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(self, user: UserDB, token: str, request: Optional[Request] = None):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(self, user: UserDB, token: str, request: Optional[Request] = None):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


def get_user_manager(user_db: TortoiseUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)
