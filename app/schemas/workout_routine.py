from app.models.workout_routine import RoutineWorkoutBase
from sqlmodel import SQLModel
from typing import Optional


class RoutineWorkoutUpdate(SQLModel):
    order: Optional[int]
    sets: Optional[int]
    reps: Optional[int]

class RoutineWorkoutCreate(RoutineWorkoutBase):
    order: Optional[int] = 0

class RoutineWorkoutResponse(SQLModel):
    id: int
    order:int
    sets: int
    reps: int