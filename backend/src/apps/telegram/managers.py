from fastapi.params import Depends

from core.users.managers import UserDatabase, UserManager
from core.users.models import User
from apps.telegram.models import Telegram


def get_telegram_db():
    yield UserDatabase(User, Telegram)


async def get_telegram_manager(user_db: UserDatabase = Depends(get_telegram_db)):
    yield UserManager(user_db)
