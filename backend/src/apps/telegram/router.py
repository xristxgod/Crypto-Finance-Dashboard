from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.responses import JSONResponse

from tortoise import transactions

from apps.auth.config import current_active_user
from apps.users.utils import get_user_or_404
from apps.telegram import schemas
from .models import Telegram, TelegramReferralLink


router = APIRouter(
    dependencies=[Depends(current_active_user)],
)


@router.get(
    '/link',
    response_model=schemas.BodyTelegramReferralLink,
    response_class=JSONResponse
)
async def telegram_link(user=Depends(get_user_or_404)):
    referral = await TelegramReferralLink.filter(user=user).exists()
    if referral:
        return schemas.BodyTelegramReferralLink(
            url=referral.url
        )
    elif not await Telegram.filter(user=user).exists():
        async with transactions.atomic():
            referral_code = TelegramReferralLink(user=user)
            await referral_code.save()
            return schemas.BodyTelegramReferralLink()

    return JSONResponse({
        'message': 'This account is already in the system',
        'chat_id': user.telegram.chat_id,
    })


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
