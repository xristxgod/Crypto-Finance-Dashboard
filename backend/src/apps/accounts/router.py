from fastapi import APIRouter
from fastapi.params import Depends

from apps.auth.config import current_active_user

router = APIRouter()


@router.on_event("startup")
async def on_startup():
    from tortoise import transactions
    from apps.accounts.models import Service
    from apps.accounts.credential_manager import get_active_managers

    cls_managers = await get_active_managers()
    async with transactions.in_transaction('default'):
        for obj in await Service.all():
            await obj.delete()

        for cls_manager in cls_managers:
            await Service.update_or_create(id=cls_manager.service_name, defaults=dict(
                credential_manager_cls_name=cls_manager.name()
            ))


@router.get(
    '/'
)
async def get_accounts(user=Depends(current_active_user)):
    pass
