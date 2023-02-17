import uuid

from fastapi import status
from fastapi.params import Depends
from fastapi.exceptions import HTTPException
from fastapi_users import models
from fastapi_users.manager import BaseUserManager, UserNotExists

from apps.auth.managers import get_user_manager


async def get_user_or_404(
    id: uuid.UUID4,
    user_manager: BaseUserManager[models.UC, models.UD] = Depends(get_user_manager),
) -> models.UD:
    try:
        return await user_manager.get(id)
    except UserNotExists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
