from sqlmodel import Session, select, func
from app.dependencies.session import SessionDep
from app.models.workout_routine import RoutineWorkoutBase, RoutineWorkout
from typing import Optional, Tuple
from app.utilities.pagination import Pagination
from app.schemas.routine_workout import RoutineWorkoutUpdate
import logging

logger = logging.getLogger(__name__)

class RoutineWorkoutRepository:
    def __init__(self, db:SessionDep):
        self.db = db

    def create(self, RoutineWorkout_data: RoutineWorkoutBase) -> Optional[RoutineWorkout]:
        try:
            routine_workout_db = RoutineWorkout.model_validate(RoutineWorkout_data)
            self.db.add(routine_workout_db)
            self.db.commit()
            self.db.refresh(routine_workout_db)
            return routine_workout_db
        except Exception as e:
            logger.error(f"An error occurred while saving Routine: {e}")
            self.db.rollback()
            raise

    def search_RoutineWorkouts(self, query: int, page:int=1, limit:int=10) -> Tuple[list[RoutineWorkout], Pagination]:
        offset = (page - 1) * limit
        db_qry = select(RoutineWorkout)
        if query:
            db_qry = db_qry.where(
                RoutineWorkout.sets.ilike(f"%{query}%")
            )
        count_qry = select(func.count()).select_from(db_qry.subquery())
        count_todos = self.db.exec(count_qry).one()

        Routines = self.db.exec(db_qry.offset(offset).limit(limit)).all()
        pagination = Pagination(total_count=count_todos, current_page=page, limit=limit)

        return Routines, pagination

    def get_by_id(self, RoutineWorkout_id: int) -> Optional[RoutineWorkout]:
        return self.db.get(RoutineWorkout, RoutineWorkout_id)

    def get_all_RoutineWorkouts(self) -> list[Routine]:
        return self.db.exec(select(RoutineWorkout)).all()

    def update_RoutineWorkout(self, RoutineWorkout_id:int, RoutineWorkout_data: RoutineWorkoutUpdate)->RoutineWorkout:
        routine_workout = self.db.get(RoutineWorkout, RoutineWorkout_id)
        if not routine_workout:
            raise Exception("Invalid Routine Workout id given")
        if RoutineWorkout_data.order:
            routine_workout.order = RoutineWorkout_data.order
        if RoutineWorkout_data.sets:
            routine_workout.sets = RoutineWorkout_data.sets
        if RoutineWorkout_data.reps:
            routine_workout.reps = RoutineWorkout_data.reps

        try:
            self.db.add(routine_workout)
            self.db.commit()
            self.db.refresh(routine_workout)
            return routine_workout
        except Exception as e:
            logger.error(f"An error occurred while updating Routine Workout: {e}")
            self.db.rollback()
            raise

    def delete_RoutineWorkout(self, RoutineWorkout_id: int):
        routine_workout = self.db.get(RoutineWorkout, RoutineWorkout_id)
        if not routine_workout:
            raise Exception("Routine Workout doesn't exist")
        try:
            self.db.delete(routine_workout)
            self.db.commit()
        except Exception as e:
            logger.error(f"An error occurred while deleting Routine Workout: {e}")
            self.db.rollback()
            raise
