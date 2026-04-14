from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .workout_routine import RoutineWorkout


class RoutineBase(SQLModel):
    name: str
    description: str = ""
    user_id: int = Field(foreign_key="user.id")


class Routine(RoutineBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user: Optional["User"] = Relationship(back_populates="routines")
    workout_links: list["RoutineWorkout"] = Relationship(back_populates="routine")
