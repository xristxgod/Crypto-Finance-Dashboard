import fastapi

from core import database
from config import settings

app = fastapi.FastAPI(
    title=settings.TITLE,
    version=settings.VERSION
)

database.connect(app)
