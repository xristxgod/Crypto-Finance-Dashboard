from fastapi import APIRouter
from fastapi import status
from fastapi.params import Depends
from fastapi.requests import Request
from fastapi.responses import Response

from fastapi_users.manager import BaseUserManager
from fastapi_users.models import UP, ID

from core.users.config import current_active_user
from core.users.managers import get_user_manager
from core.users import schemas
from core.users import services

router = APIRouter(
    dependencies=[Depends(current_active_user)],
)


@router.on_event('startup')
async def setup_language():
    from tortoise import transactions
    from config import settings
    from core.users.models import Language

    async with transactions.in_transaction('default'):
        if await Language.filter(id__in=settings.LANGUAGES).count() != len(settings.LANGUAGES):
            await Language.all().delete()
            await Language.bulk_create([
                Language(id=language_id)
                for language_id in settings.LANGUAGES
            ])


@router.get(
    '/me',
    response_model=schemas.BodyUser,
)
async def me(user: schemas.BodyUser = Depends(current_active_user)):
    return user


@router.patch(
    '/me',
    response_model=schemas.BodyUser,
)
async def update_me(
        body: schemas.BodyUpdateUser,
        request: Request,
        user: schemas.BodyUser = Depends(current_active_user),
        user_manager: BaseUserManager[UP, ID] = Depends(get_user_manager),
):
    return await services.update_user(body, request, user, user_manager)


@router.delete(
    '/me',
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def delete_me(
        user: schemas.BodyUser = Depends(current_active_user),
        user_manager: BaseUserManager[UP, ID] = Depends(get_user_manager),
):
    await services.delete_user(user, user_manager)
