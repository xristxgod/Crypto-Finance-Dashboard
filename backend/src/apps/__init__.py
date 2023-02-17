from fastapi.routing import APIRouter

from . import users
from . import auth

__all__ = (
    'connector',
)

connector = APIRouter(
    prefix='/v1',
)

connector.include_router(users.router)
connector.include_router(auth.router)
