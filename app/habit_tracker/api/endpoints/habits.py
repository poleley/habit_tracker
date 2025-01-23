from fastapi import APIRouter, Depends, status

from app.habit_tracker.api import deps
from app.habit_tracker.api.deps import get_token
from app.habit_tracker.entity.habits import HabitCreate

router = APIRouter(prefix="/habits", tags=["Habits"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_habit(
    service: deps.LeadsDEP, data: HabitCreate, payload: dict = Depends(get_token)
):
    return await service.create_lead(data=data, user_id=payload["uuid"])
