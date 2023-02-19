from fastapi.params import Depends
from fastapi.routing import APIRouter

from .config import fastapi_users, get_current_superuser, cookie_authentication, jwt_authentication

router = APIRouter()

router.include_router(
    # fastapi_users.get_auth_router(jwt_authentication),
    fastapi_users.get_auth_router(cookie_authentication),
)

router.include_router(
    fastapi_users.get_register_router(),
)
