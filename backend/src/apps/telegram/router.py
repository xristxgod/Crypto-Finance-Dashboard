from fastapi import APIRouter
from fastapi.params import Depends

from apps.auth.config import current_active_user
from apps.users.utils import get_user_or_404
from apps.telegram import schemas


router = APIRouter(
    dependencies=[Depends(current_active_user)],
)


@router.patch(
    '/{id:uuid}',
    response_model=schemas.TelegramDB,
)
async def update_telegram(body: schemas.TelegramDB, user=Depends(get_user_or_404)):
    pass


@router.delete(
    '/{id:uuid}'
)
async def delete_telegram(user=Depends(get_user_or_404)):
    pass
