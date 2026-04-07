from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from models.workout import Workout
from models.workout_routine import RoutineWorkout

class RoutineBase(SQLModel):
    name: str
    description: str
    user_id: int = Field(foreign_key="user.id")


class Routine(RoutineBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    workouts: list['Workout'] = Relationship(back_populates=("routines"), link_model=RoutineWorkout)