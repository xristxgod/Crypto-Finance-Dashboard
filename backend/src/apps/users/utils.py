from typing import cast

from pydantic import UUID4
from fastapi.params import Depends
from fastapi_users import models
from fastapi_users.manager import BaseUserManager
from fastapi_users.db import TortoiseUserDatabase
from tortoise.contrib.pydantic.base import PydanticModel

from apps.users.managers import UserManager
from apps.users.schemas import UserDB
from apps.users.models import User


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


def get_user_manager(user_db: TortoiseUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


async def get_user_or_404(
    id: UUID4,
    user_manager: BaseUserManager[models.UC, models.UD] = Depends(get_user_manager),
) -> models.UD:
    return await user_manager.get(id)
