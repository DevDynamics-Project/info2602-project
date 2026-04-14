from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .routine import Routine
    from .workout import Workout


class RoutineWorkoutBase(SQLModel):
    routine_id: Optional[int] = Field(default=None, foreign_key="routine.id", primary_key=True)
    workout_id: Optional[int] = Field(default=None, foreign_key="workout.id", primary_key=True)
    order: int = 0
    sets: int = 3
    reps: int = 10


class RoutineWorkout(RoutineWorkoutBase, table=True):
    routine: Optional["Routine"] = Relationship(back_populates="workout_links")
    workout: Optional["Workout"] = Relationship(back_populates="routine_links")
