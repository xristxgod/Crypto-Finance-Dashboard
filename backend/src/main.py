import fastapi

import apps
from core import database
from config import settings

app = fastapi.FastAPI(
    title=settings.TITLE,
    version=settings.VERSION
)

database.connect(app)

app.include_router(apps.connector, prefix='/api')
app.include_router(apps.connector_v1, prefix='/api/v1')
