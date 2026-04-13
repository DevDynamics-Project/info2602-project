from app.models.workout import WorkoutBase
from sqlmodel import SQLModel
from typing import Optional


class WorkoutUpdate(SQLModel):
    difficulty: Optional[str]
    duration: Optional[str]
    description: Optional[str]

class WorkoutCreate(WorkoutBase):
    difficulty:str = "moderate"

class WorkoutResponse(SQLModel):
    id: int
    name:str
    description: str
    difficulty: str
    duration: str
    
