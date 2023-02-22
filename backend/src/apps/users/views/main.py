from fastapi import status
from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.params import Depends
from fastapi_users import models
from fastapi_users.manager import BaseUserManager

from apps.users import schemas
from apps.users.config import current_active_user, current_superuser
from apps.users.services import user_services as services
from apps.users.utils import get_user_manager, get_user_or_404

router = APIRouter(
    dependencies=[Depends(current_active_user)],
)


@router.get(
    "/me", response_model=schemas.UserDB,
    response_model_exclude={'hashed_password'},
)
async def me(user: schemas.UserDB = Depends(current_active_user)):
    return user


@router.patch(
    "/{id:uuid}",
    response_model=schemas.BodyUser,
    dependencies=[Depends(current_superuser)],
)
@router.patch(
    '/me',
    response_model=schemas.BodyUser,
)
async def update_user(
        body: schemas.BodyUserUpdate,
        request: Request,
        user=Depends(get_user_or_404),
        user_manager: BaseUserManager[models.UC, models.UD] = Depends(get_user_manager),
):
    return await services.update_user(body, user, user_manager, request)


@router.delete(
    "/{id:uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    dependencies=[Depends(current_superuser)],
)
@router.delete(
    "/me/delete",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def delete_me(
        user: schemas.UserDB = Depends(current_active_user),
        user_manager: BaseUserManager[models.UC, models.UD] = Depends(get_user_manager),
):
    await services.delete_user(user, user_manager)
