from pydantic import UUID4

from apps.accounts.credential_manager import Keys
from apps.accounts import schemas
from apps.accounts.models import Account


async def get_account_detail(account: Account):
    return schemas.BodyAccountDetail(
        id=account.id,
        name=account.name,
        service=account.service.name,
        created_at=account.created_at,
        modified_at=account.modified_at,
        keys=account.get_keys(),
    )


async def create_account(name: str, keys: Keys, service_id: str, user_id: UUID4):
    from tortoise import transactions
    async with transactions.in_transaction('default'):
        account = await Account.create(
            name=name,
            service_id=service_id,
            user_id=user_id
        )
        await account.set_keys(
            public=keys.public,
            secret=keys.secret,
        )

    return await get_account_detail(account)
