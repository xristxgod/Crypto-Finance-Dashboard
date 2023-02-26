from __future__ import absolute_import

from fastapi import APIRouter

from .users import routers as u_router

router = APIRouter()

# Auth
router.include_router(u_router.auth_router, prefix='/auth', tags=['Auth'])
# Users
router.include_router(u_router.users_router, prefix='/users', tags=['Users'])
