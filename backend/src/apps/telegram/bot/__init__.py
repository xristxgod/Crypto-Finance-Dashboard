from .app import dp, app as bot
from apps.telegram.views.bot import router

__all__ = (
    'bot',
    'dp',
    'router',
)
