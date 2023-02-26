from typing import NoReturn

from fastapi import status
from fastapi.requests import Request
from fastapi.exceptions import HTTPException
from fastapi_users.router.common import ErrorCode
from fastapi_users.manager import BaseUserManager
from fastapi_users.exceptions import InvalidPasswordException, UserAlreadyExists

from core.users import schemas


async def delete_user(user: schemas.BodyUser, manager: BaseUserManager) -> NoReturn:
    await manager.delete(user)


async def update_user(body: schemas.BodyUpdateUser,
                      request: Request,
                      user: schemas.BodyUser,
                      user_manager: BaseUserManager) -> schemas.BodyUser:
    try:
        return await user_manager.update(body, user, safe=False, request=request)
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
