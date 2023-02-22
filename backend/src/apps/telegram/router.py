from fastapi import APIRouter
from fastapi.params import Depends

from tortoise import transactions

from apps.users.config import current_active_user
from apps.users.utils import get_user_or_404
from apps.telegram import schemas
from .models import Telegram, TelegramReferralLink


router = APIRouter(
    dependencies=[Depends(current_active_user)],
)


@router.get(
    '/',
    response_model=schemas.TelegramDB | schemas.BodyTelegramReferralLink,
)
async def get_telegram(user=Depends(current_active_user)):
    referral = await TelegramReferralLink.filter(user_id=user.id)
    if referral:
        return schemas.BodyTelegramReferralLink(
            url=referral[0].url
        )
    elif not await Telegram.filter(user_id=user.id).exists():
        async with transactions.in_transaction('default'):
            referral_code = TelegramReferralLink(user_id=user.id)

            await referral_code.save()
            return schemas.BodyTelegramReferralLink(url=referral_code.url)

    return await schemas.TelegramDB.from_queryset_single(Telegram.get(user_id=user.id))


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
