from fastapi.params import Depends
from fastapi_users import models
from fastapi_users.manager import BaseUserManager
from pydantic import UUID4

from apps.users.managers import get_user_manager


async def get_user_or_404(
    id: UUID4,
    user_manager: BaseUserManager[models.UC, models.UD] = Depends(get_user_manager),
) -> models.UD:
    return await user_manager.get(id)
