from typing import Optional

from fastapi.params import Depends
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users.manager import BaseUserManager, UserNotExists
from fastapi_users import models, password
from fastapi_users.db import TortoiseUserDatabase

from config import settings
from apps.users.schemas import BodyUserCreate, UserDB
from apps.auth.utils import get_user_db

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

    async def get_by_username(self, user_username: str):
        user = await self.user_db.get_by_username(user_username)

        if user is None:
            raise UserNotExists()

        return user

    async def authenticate(
        self, credentials: OAuth2PasswordRequestForm
    ) -> Optional[models.UD]:
        try:
            if credentials.username.find('@') > 1:
                user = await self.get_by_email(credentials.username)
            else:
                user = await self.get_by_username(credentials.username)
        except UserNotExists:
            # Run the hasher to mitigate timing attack
            # Inspired from Django: https://code.djangoproject.com/ticket/20760
            password.get_password_hash(credentials.password)
            return None

        verified, updated_password_hash = password.verify_and_update_password(
            credentials.password, user.hashed_password
        )
        if not verified:
            return None
        # Update password hash to a more robust one if needed
        if updated_password_hash is not None:
            user.hashed_password = updated_password_hash
            await self.user_db.update(user)

        return user


def get_user_manager(user_db: TortoiseUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)
