from typing import Optional

from fastapi.requests import Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users.manager import BaseUserManager, UserNotExists
from fastapi_users import models, password

from config import settings
from apps.users.schemas import BodyUserCreate, UserDB

__all__ = (
    'UserManager',
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
