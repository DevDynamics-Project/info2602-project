from sqlmodel import Session, select, func
from app.dependencies.session import SessionDep
from app.models.workout import WorkoutBase, Workout
from typing import Optional, Tuple
from app.utilities.pagination import Pagination
from app.schemas.workout import WorkoutUpdate
import logging

logger = logging.getLogger(__name__)

class WorkoutRepository:
    def __init__(self, db:SessionDep):
        self.db = db

    def create(self, Workout_data: WorkoutBase) -> Optional[Workout]:
        try:
            workout_db = Workout.model_validate(Workout_data)
            self.db.add(workout_db)
            self.db.commit()
            self.db.refresh(workout_db)
            return workout_db
        except Exception as e:
            logger.error(f"An error occurred while saving Workout: {e}")
            self.db.rollback()
            raise

    def search_Workouts(self, query: str, page:int=1, limit:int=10) -> Tuple[list[Workout], Pagination]:
        offset = (page - 1) * limit
        db_qry = select(Workout)
        if query:
            db_qry = db_qry.where(
                Workout.name.ilike(f"%{query}%")
            )
        count_qry = select(func.count()).select_from(db_qry.subquery())
        count_todos = self.db.exec(count_qry).one()

        Workouts = self.db.exec(db_qry.offset(offset).limit(limit)).all()
        pagination = Pagination(total_count=count_todos, current_page=page, limit=limit)

        return Workouts, pagination

    def get_by_Workoutname(self, Workoutname: str) -> Optional[Workout]:
        return self.db.exec(select(Workout).where(Workout.name == Workoutname)).one_or_none()

    def get_by_id(self, Workout_id: int) -> Optional[Workout]:
        return self.db.get(Workout, Workout_id)

    def get_all_Workouts(self) -> list[Workout]:
        return self.db.exec(select(Workout)).all()

    def update_Workout(self, Workout_id:int, Workout_data: WorkoutUpdate)->Workout:
        workout = self.db.get(Workout, Workout_id)
        if not workout:
            raise Exception("Invalid Workout id given")
        if Workout_data.difficulty:
            workout.difficulty = Workout_data.difficulty
        if Workout_data.duration:
            workout.duration = Workout_data.duration
        if Workout_data.description:
            workout.description = Workout_data.description

        try:
            self.db.add(workout)
            self.db.commit()
            self.db.refresh(workout)
            return workout
        except Exception as e:
            logger.error(f"An error occurred while updating Workout: {e}")
            self.db.rollback()
            raise

    def delete_Workout(self, Workout_id: int):
        workout = self.db.get(Workout, Workout_id)
        if not workout:
            raise Exception("Workout doesn't exist")
        try:
            self.db.delete(workout)
            self.db.commit()
        except Exception as e:
            logger.error(f"An error occurred while deleting Workout: {e}")
            self.db.rollback()
            raise
