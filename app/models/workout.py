from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from app.models.workout_routine import RoutineWorkout


class WorkoutBase(SQLModel):
    name: str = Field(index=True)
    description: str
    duration: int   # in minutes
    difficulty: str
    muscle_group: str


class Workout(WorkoutBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    routines: list["Routine"] = Relationship(back_populates=("workouts"), link_model=RoutineWorkout)