from sqlmodel import SQLModel
from typing import Optional
from app.schemas.workout import WorkoutResponse


class RoutineCreate(SQLModel):
    name: str
    description: str = ""


class AddWorkoutRequest(SQLModel):
    workout_id: int
    sets: int = 3
    reps: int = 10
    order: int = 0


class UpdateWorkoutInRoutineRequest(SQLModel):
    sets: Optional[int] = None
    reps: Optional[int] = None
    order: Optional[int] = None


class RemixWorkoutRequest(SQLModel):
    new_workout_id: int


class RoutineWorkoutResponse(SQLModel):
    workout: WorkoutResponse
    sets: int
    reps: int
    order: int


class RoutineResponse(SQLModel):
    id: int
    name: str
    description: str
    user_id: int
    workouts: list[RoutineWorkoutResponse] = []
