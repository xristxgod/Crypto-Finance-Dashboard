from .main import router as telegram_router
from .bot import router as bot_router

__all__ = (
    'telegram_router',
    'bot_router',
)
