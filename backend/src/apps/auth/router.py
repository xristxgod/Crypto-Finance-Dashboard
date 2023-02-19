from fastapi.routing import APIRouter

from .config import fastapi_users, jwt_authentication

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(jwt_authentication),
)

router.include_router(
    fastapi_users.get_register_router(),
)
