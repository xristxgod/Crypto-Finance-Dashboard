from fastapi.routing import APIRouter

from .users import views as users_views
from .telegram import views as telegram_views
from . import accounts

__all__ = (
    'connector_v1',
)

webhooks = APIRouter()
connector = APIRouter()
connector_v1 = APIRouter()

# Connector V1
connector_v1.include_router(
    users_views.users_router,
    prefix='/users',
    tags=['Users'],
)
connector_v1.include_router(
    telegram_views.telegram_router,
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
    users_views.auth_router,
    prefix='/auth',
    tags=['Auth'],
)
# Webhooks
webhooks.include_router(telegram_views.bot_router, prefix='/telegram')
