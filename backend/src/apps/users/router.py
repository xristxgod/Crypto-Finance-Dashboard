from fastapi import status
from fastapi.routing import APIRouter
from fastapi.requests import Request
from fastapi.params import Depends
from fastapi.exceptions import HTTPException
from fastapi_users import models
from fastapi_users.router.common import ErrorCode
from fastapi_users.manager import BaseUserManager, InvalidPasswordException, UserAlreadyExists

from . import schemas
from .utils import get_user_or_404
from apps.auth.managers import get_user_manager
from apps.auth.config import get_current_active_user, get_current_superuser

router = APIRouter(
    dependencies=[Depends(get_current_active_user)],
    prefix='users/',
    tags=['Users'],
)


@router.get("/me", response_model=schemas.UserDB)
async def me(user: schemas.UserDB = Depends(get_current_active_user)):
    return user


@router.patch(
    "/{id:uuid}",
    response_model=schemas.BodyUser,
    dependencies=[Depends(get_current_superuser)],
)
async def update_user(
    body: schemas.BodyUserUpdate,
    request: Request,
    user=Depends(get_user_or_404),
    user_manager: BaseUserManager[models.UC, models.UD] = Depends(get_user_manager),
):
    try:
        return await user_manager.update(
            body, user, safe=False, request=request
        )
    except InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                "reason": e.reason,
            },
        )
    except UserAlreadyExists:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS,
        )


@router.delete(
    "/{id:uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=schemas.ResponseSuccess,
    dependencies=[Depends(get_current_superuser)],
)
async def delete_user(
    user=Depends(get_user_or_404),
    user_manager: BaseUserManager[models.UC, models.UD] = Depends(get_user_manager),
):
    await user_manager.delete(user)
    return schemas.ResponseSuccess()
