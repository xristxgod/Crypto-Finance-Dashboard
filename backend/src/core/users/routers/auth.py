from fastapi import APIRouter

from core.users.schemas import BodyUser, BodyCreateUser
from core.users.config import fastapi_users, cookie_authentication

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(cookie_authentication),
)

router.include_router(
    fastapi_users.get_register_router(
        user_schema=BodyUser,
        user_create_schema=BodyCreateUser,
    ),
)
