from __future__ import absolute_import

from fastapi import APIRouter

from . import auth


connector = APIRouter()

connector.include_router(
    auth.router,
)
