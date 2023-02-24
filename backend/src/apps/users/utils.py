from pydantic import UUID4
from fastapi.params import Depends
from fastapi_users import models
from fastapi_users.manager import BaseUserManager
from fastapi_users.db import TortoiseUserDatabase

from apps.users.schemas import UserDB
from apps.users.models import User


def get_user_db():
    from apps.users.managers import CustomTortoiseUserDatabase
    yield CustomTortoiseUserDatabase(UserDB, User)


def get_user_manager(user_db: TortoiseUserDatabase = Depends(get_user_db)):
    from apps.users.managers import UserManager
    yield UserManager(user_db)


async def get_user_or_404(
    id: UUID4,
    user_manager: BaseUserManager[models.UC, models.UD] = Depends(get_user_manager),
) -> models.UD:
    return await user_manager.get(id)
