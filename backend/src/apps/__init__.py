from fastapi.routing import APIRouter

from . import users
from . import auth

__all__ = (
    'connector_v1',
)

connector = APIRouter()
connector_v1 = APIRouter()

# Connector V1
connector_v1.include_router(
    users.router,
    prefix='/users',
    tags=['Users'],
)
# Connector
connector.include_router(
    auth.router,
    prefix='/auth',
    tags=['Auth'],
)
