from fastapi import status
from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.responses import Response

from core.users.schemas import BodyUser
from core.users.config import current_active_user
from core.users.managers import UserManager
from apps.telegram.managers import get_telegram_manager
from apps.telegram import services
from apps.telegram.schemas import BodyTelegram, ResponseTelegramReferralLink

router = APIRouter()


@router.get(
    '/',
    response_model=BodyTelegram | ResponseTelegramReferralLink
)
async def get_telegram(
        user: BodyUser = Depends(current_active_user),
        telegram_manager: UserManager = Depends(get_telegram_manager),
):
    return await services.get_telegram(user, telegram_manager)


@router.delete(
    '/',
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def delete_telegram(
        user: BodyUser = Depends(current_active_user),
        telegram_manager: UserManager = Depends(get_telegram_manager),
):
    return await telegram_manager.delete_sub_model(user_id=user.id)
