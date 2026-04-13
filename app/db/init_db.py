from app.database import engine
from sqlmodel import SQLModel
from app.db.seed_workouts import seed_workouts

def init_db():
    SQLModel.metadata.create_all(engine)
    seed_workouts()