from pydantic import UUID4
from fastapi.params import Depends

from apps.users.config import current_active_user
from .models import Account


async def get_account_or_404(
    id: UUID4,
    user=Depends(current_active_user)
) -> Account:
    return await Account.get(id=id, user_id=user.id)
