from typing import cast

from tortoise.contrib.pydantic.base import PydanticModel
from fastapi_users.db import TortoiseUserDatabase
from fastapi_users import models

from apps.users.schemas import UserDB
from apps.users.models import User

__all__ = (
    'get_user_db',
)


class CustomTortoiseUserDatabase(TortoiseUserDatabase):

    async def get_by_username(self, username: str):
        query = self.model.filter(username__iexact=username).first()

        if self.oauth_account_model is not None:
            query = query.prefetch_related("oauth_accounts")

        user = await query

        if user is None:
            return None

        pydantic_user = await cast(PydanticModel, self.user_db_model).from_tortoise_orm(
            user
        )

        return cast(models.UD, pydantic_user)


def get_user_db():
    yield CustomTortoiseUserDatabase(UserDB, User)
