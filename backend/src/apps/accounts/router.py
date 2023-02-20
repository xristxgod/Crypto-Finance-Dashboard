from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.params import Depends

from apps.auth.config import current_active_user
from apps.accounts.models import Account
from apps.accounts.models import Service
from apps.accounts import schemas
from apps.accounts.utils import get_account_or_404

router = APIRouter()


@router.on_event("startup")
async def on_startup():
    from tortoise import transactions
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
    '/services',
    response_model=list[schemas.ServiceDB]
)
async def get_active_services():
    return await schemas.ServiceDB.from_queryset(Service.all())


@router.get(
    '/',
    response_model=list[schemas.AccountDB],
)
async def get_accounts(user=Depends(current_active_user)):
    return await schemas.AccountDB.from_queryset(Account.filter(user_id=user.id))


@router.get(
    '/{id:uuid}',
    response_model=schemas.BodyAccountDetail,
    dependencies=[Depends(current_active_user)],
)
async def get_account_detail(account: Account = Depends(get_account_or_404)):
    return schemas.BodyAccountDetail(
        id=account.id,
        name=account.name,
        service=account.service.name,
        created_at=account.created_at,
        modified_at=account.modified_at,
        keys=account.get_keys(),
    )
