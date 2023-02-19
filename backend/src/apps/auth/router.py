from fastapi.routing import APIRouter

from .config import fastapi_users, cookie_authentication

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(cookie_authentication),
)

router.include_router(
    fastapi_users.get_register_router(),
)
