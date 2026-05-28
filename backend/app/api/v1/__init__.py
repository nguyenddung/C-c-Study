"""API v1 routers barrel."""
from fastapi import APIRouter

from .auth import router as auth_router
from .groups import router as groups_router
from .matching import router as matching_router
from .messages import router as messages_router
from .notifications import router as notifications_router
from .profiles import router as profiles_router
from .uploads import router as uploads_router
from .users import router as users_router

v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(auth_router)
v1_router.include_router(users_router)
v1_router.include_router(profiles_router)
v1_router.include_router(matching_router)
v1_router.include_router(groups_router)
v1_router.include_router(messages_router)
v1_router.include_router(notifications_router)
v1_router.include_router(uploads_router)