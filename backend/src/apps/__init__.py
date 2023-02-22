from fastapi.routing import APIRouter

from . import users
from . import telegram
from . import accounts

__all__ = (
    'connector_v1',
)

webhooks = APIRouter()
connector = APIRouter()
connector_v1 = APIRouter()

# Connector V1
connector_v1.include_router(
    users.users_router,
    prefix='/users',
    tags=['Users'],
)
connector_v1.include_router(
    telegram.router,
    prefix='/telegram',
    tags=['Telegram'],
)
connector_v1.include_router(
    accounts.router,
    prefix='/accounts',
    tags=['Accounts'],
)
# Connector
connector.include_router(
    users.auth_router,
    prefix='/auth',
    tags=['Auth'],
)
# Webhooks
webhooks.include_router(telegram.bot.router, prefix='/telegram')
