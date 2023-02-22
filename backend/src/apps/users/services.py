from fastapi import status
from fastapi.requests import Request
from fastapi.exceptions import HTTPException
from fastapi_users.router.common import ErrorCode
from fastapi_users.manager import BaseUserManager, InvalidPasswordException, UserAlreadyExists

from .schemas import UserDB, BodyUserUpdate


async def delete_user(user: UserDB, manager: BaseUserManager):
    await manager.delete(user)


async def update_user(body: BodyUserUpdate, user: UserDB, manager: BaseUserManager, request: Request):
    try:
        return await manager.update(
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
