from typing import Type, TypeVar, Optional, NoReturn, Any

from pydantic import UUID4
from fastapi.params import Depends
from fastapi.requests import Request

from fastapi_users import models
from fastapi_users.manager import BaseUserManager, UUIDIDMixin
from fastapi_users.exceptions import UserNotExists
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi_users_tortoise import TortoiseUserDatabase, UP_TORTOISE

from config import settings
from core.users.models import User, SubModel
from core.users import BodySubModel

SM = TypeVar("SM", bound=SubModel)
BSM = TypeVar("BSM", bound=BodySubModel)


class SubModelNotExits(UserNotExists):
    pass


class UserDatabase(TortoiseUserDatabase):
    def __init__(
            self,
            user_model: Type[UP_TORTOISE],
            sub_model: Optional[Type[SM]] = None,
            **kwargs,
    ):
        super().__init__(user_model, **kwargs)
        self.sub_model = sub_model

    async def get_by_username(self, username: str):
        query = self.user_model.filter(username__iexact=username).first()

        if self.oauth_account_model is not None:
            query = query.prefetch_related("oauth_accounts")

        return await query

    async def create_sub_model(self, user_id: UUID4, create_dict: dict[str, Any]) -> SM:
        sub_model = self.sub_model(**create_dict, user_id=user_id)
        await sub_model.save()
        await sub_model.refresh_from_db()
        return sub_model

    async def get_sub_model(self, user_id: UUID4, model_id: Optional[models.ID] = None) -> SM:
        sub_model = self.sub_model.filter(user_id=user_id)
        if model_id:
            sub_model = sub_model.filter(id=model_id)

        return await sub_model.first()

    async def get_sub_models(self, user_id: UUID4) -> list[SM]:
        sub_models = self.sub_model.filter(user_id=user_id).all()
        return await sub_models

    async def delete_sub_model(self, user_id: UUID4, model_id: Optional[models.ID] = None) -> NoReturn:
        sub_model = self.sub_model.filter(user_id=user_id)
        if model_id:
            sub_model = sub_model.filter(id=model_id)
        await sub_model.first().delete()


class UserManager(UUIDIDMixin, BaseUserManager[User, UUID4]):
    reset_password_token_secret = settings.AUTH_SECRET_KEY
    verification_token_secret = settings.AUTH_SECRET_KEY

    user_db: UserDatabase

    async def get_by_username(self, user_username: str):
        user = await self.user_db.get_by_username(user_username)

        if user is None:
            raise UserNotExists()

        return user

    async def create_sub_model(
            self, user_id: UUID4, sub_model_create: BSM,
            safe: bool = False, request: Optional[Request] = None
    ) -> SM:

        user = await self.user_db.get(sub_model_create.user_id)
        if user is None:
            raise SubModelNotExits

        sub_model_dict = (
            sub_model_create.create_update_dict()
            if safe
            else sub_model_create.create_update_dict_superuser()
        )

        created_sub_model = await self.user_db.create_sub_model(user_id, sub_model_dict)

        await self.on_after_create_sub_model(created_sub_model, request)

        return created_sub_model

    async def get_sub_model(self, user_id: UUID4, model_id: Optional[models.ID] = None) -> SM:
        sub_model = await self.user_db.get_sub_model(user_id, model_id)
        if sub_model is None:
            raise SubModelNotExits()
        return sub_model

    async def get_sub_models(self, user_id: UUID4) -> list[SM]:
        sub_models = await self.user_db.get_sub_models(user_id)
        if sub_models:
            raise SubModelNotExits()
        return sub_models

    async def delete_sub_model(
            self, user_id: UUID4,
            model_id: Optional[models.ID] = None
    ) -> NoReturn:
        await self.user_db.delete_sub_model(user_id, model_id)

    async def on_after_create_sub_model(
        self, sub_model: SM, request: Optional[Request] = None
    ) -> None:
        pass

    async def authenticate(
        self, credentials: OAuth2PasswordRequestForm
    ) -> Optional[models.UP]:
        """
        Authenticate and return a user following an email and a password.

        Will automatically upgrade password hash if necessary.

        :param credentials: The user credentials.
        """
        try:
            if credentials.username.find('@') > 1:
                user = await self.get_by_email(credentials.username)
            else:
                user = await self.get_by_username(credentials.username)
        except UserNotExists:
            self.password_helper.hash(credentials.password)
            return None

        verified, updated_password_hash = self.password_helper.verify_and_update(
            credentials.password, user.hashed_password
        )
        if not verified:
            return None

        if updated_password_hash is not None:
            await self.user_db.update(user, {"hashed_password": updated_password_hash})

        return user


def get_user_db():
    yield UserDatabase(User)


def get_user_manager(user_db: UserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)
