from fastapi.routing import APIRouter

from . import users
from . import telegram
from . import auth

__all__ = (
    'connector_v1',
)

webhooks = APIRouter()
connector = APIRouter()
connector_v1 = APIRouter()

# Connector V1
connector_v1.include_router(
    users.router,
    prefix='/users',
    tags=['Users'],
)
connector_v1.include_router(
    telegram.router,
    prefix='/telegram',
    tags=['Telegram'],
)
# Connector
connector.include_router(
    auth.router,
    prefix='/auth',
    tags=['Auth'],
)
# Webhooks
webhooks.include_router(telegram.bot.router, prefix='/telegram')
