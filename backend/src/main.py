from fastapi import FastAPI

from core import router as c_router
from apps import router as a_router

import core.database as database
import core.caches as caches

app = FastAPI()

database.connect(app)


@app.on_event("startup")
async def startup():
    await caches.connect()

# Core
app.include_router(c_router, prefix='/api')
# Apps
app.include_router(a_router, prefix='/api')
