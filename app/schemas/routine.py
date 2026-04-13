from app.models.routine import RoutineBase
from sqlmodel import SQLModel
from typing import Optional


class RoutineUpdate(SQLModel):
    name: Optional[str]
    description: Optional[str]

class RoutineCreate(RoutineBase):
    description: Optional[str] = ""

class RoutineResponse(SQLModel):
    id: int
    name:str
    description: str