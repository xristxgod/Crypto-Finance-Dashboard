from .auth import router as auth_router
from .main import router as users_router

__all__ = (
    'users_router',
    'auth_router',
)
