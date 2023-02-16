from fastapi import FastAPI

from src import core
from src import apps


app = FastAPI()

# Core
app.include_router(
    core.connector,
)
