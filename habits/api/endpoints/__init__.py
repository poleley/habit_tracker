from fastapi import APIRouter
from habits.api.endpoints import habits, users, auth

root = APIRouter(prefix="/api/v1")
root.include_router(habits.router)
root.include_router(users.router)
root.include_router(auth.router, prefix="/auth", tags=["auth"])
