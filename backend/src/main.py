import fastapi

from apps import connector
from core import database
from config import settings

app = fastapi.FastAPI(
    title=settings.TITLE,
    version=settings.VERSION
)

database.connect(app)

app.include_router(connector, prefix='/api')
