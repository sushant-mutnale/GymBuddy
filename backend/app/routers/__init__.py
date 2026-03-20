"""
API Routers Package
"""

from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.profiles import router as profiles_router
from app.routers.matches import router as matches_router
from app.routers.workouts import router as workouts_router
from app.routers.chat import router as chat_router
from app.routers.gyms import router as gyms_router

__all__ = ["auth_router", "users_router", "profiles_router", "matches_router", "workouts_router", "chat_router", "gyms_router"]
