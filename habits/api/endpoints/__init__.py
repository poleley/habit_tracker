from fastapi import APIRouter
from habits.api.endpoints import habits

root = APIRouter(prefix="/api/v1")
root.include_router(habits.router)
