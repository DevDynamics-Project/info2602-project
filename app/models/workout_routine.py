from sqlmodel import SQLModel, Field
from typing import Optional


class RoutineWorkoutBase(SQLModel):
    routine_id: int|None = Field(primary_key=True, foreign_key='routine.id')
    workout_id: int|None = Field(primary_key=True, foreign_key='workout.id')
    order: int = 0
    sets: int = 3
    reps: int = 10


class RoutineWorkout(RoutineWorkoutBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


    