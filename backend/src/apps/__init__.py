from fastapi.routing import APIRouter

from . import users

__all__ = (
    'connector',
)

connector = APIRouter(
    prefix='/v1',
)

connector.include_router(users.router)
