from sqlmodel import Session, select
from app.models.workout import Workout, WorkoutBase
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class WorkoutRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, workout_data: WorkoutBase) -> Workout:
        try:
            workout = Workout.model_validate(workout_data)
            self.db.add(workout)
            self.db.commit()
            self.db.refresh(workout)
            return workout
        except Exception as e:
            logger.error(f"Error creating workout: {e}")
            self.db.rollback()
            raise

    def get_all(self) -> list[Workout]:
        return self.db.exec(select(Workout)).all()

    def get_by_id(self, workout_id: int) -> Optional[Workout]:
        return self.db.get(Workout, workout_id)

    def get_by_muscle_group(self, muscle_group: str) -> list[Workout]:
        return self.db.exec(
            select(Workout).where(Workout.muscle_group == muscle_group)
        ).all()

    def search(self, query: str) -> list[Workout]:
        q = f"%{query}%"
        return self.db.exec(
            select(Workout).where(
                Workout.name.ilike(q) |
                Workout.muscle_group.ilike(q) |
                Workout.difficulty.ilike(q)
            )
        ).all()

    def delete(self, workout_id: int) -> Optional[Workout]:
        workout = self.db.get(Workout, workout_id)
        if not workout:
            return None
        self.db.delete(workout)
        self.db.commit()
        return workout
