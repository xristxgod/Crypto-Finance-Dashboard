import functools
from typing import Callable

from pydantic import UUID4
from fastapi.params import Depends

from apps.auth.config import current_active_user
from .models import Account


async def get_account_or_404(
    id: UUID4,
    user=Depends(current_active_user)
) -> Account:
    return await Account.get(id=id, user_id=user.id)


def keys_validator(func: Callable):
    @functools.wraps(func)
    async def wrapper(self, public, secret):

        # TODO write keys validator by service

        return await func(self, public, secret)
    return wrapper
