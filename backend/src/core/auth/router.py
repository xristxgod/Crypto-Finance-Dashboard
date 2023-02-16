from fastapi import APIRouter

from src.core.auth import schemas
from src.core.auth import config


router = APIRouter(prefix='/auth')

router.include_router(
    config.users.get_auth_router(config.auth_backend),
    tags=["Auth"],
)

router.include_router(
    config.users.get_register_router(
        schemas.UserRead,
        schemas.UserCreate,
    ),
    tags=["Auth"],
)
