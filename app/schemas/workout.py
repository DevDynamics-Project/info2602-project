from sqlmodel import SQLModel


class WorkoutCreate(SQLModel):
    name: str
    description: str
    duration: int
    difficulty: str
    muscle_group: str


class WorkoutResponse(SQLModel):
    id: int
    name: str
    description: str
    duration: int
    difficulty: str
    muscle_group: str
