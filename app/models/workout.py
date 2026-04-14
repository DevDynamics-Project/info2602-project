from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .workout_routine import RoutineWorkout


class WorkoutBase(SQLModel):
    name: str = Field(index=True)
    description: str
    duration: int  # minutes
    difficulty: str
    muscle_group: str


class Workout(WorkoutBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    routine_links: list["RoutineWorkout"] = Relationship(back_populates="workout")
