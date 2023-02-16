from fastapi import FastAPI

import core
import apps


app = FastAPI()

# Core
app.include_router(
    core.connector,
)
