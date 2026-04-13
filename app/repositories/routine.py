from sqlmodel import Session, select, func
from app.dependencies.session import SessionDep
from app.models.routine import RoutineBase, Routine
from typing import Optional, Tuple
from app.utilities.pagination import Pagination
from app.schemas.routine import RoutineUpdate
import logging

logger = logging.getLogger(__name__)

class RoutineRepository:
    def __init__(self, db:SessionDep):
        self.db = db

    def create(self, Routine_data: RoutineBase) -> Optional[Routine]:
        try:
            routine_db = Routine.model_validate(Routine_data)
            self.db.add(routine_db)
            self.db.commit()
            self.db.refresh(routine_db)
            return routine_db
        except Exception as e:
            logger.error(f"An error occurred while saving Routine: {e}")
            self.db.rollback()
            raise

    def search_Routines(self, query: str, page:int=1, limit:int=10) -> Tuple[list[Routine], Pagination]:
        offset = (page - 1) * limit
        db_qry = select(Routine)
        if query:
            db_qry = db_qry.where(
                Routine.name.ilike(f"%{query}%") | Routine.description.ilike(f"%{query}%")
            )
        count_qry = select(func.count()).select_from(db_qry.subquery())
        count_todos = self.db.exec(count_qry).one()

        Routines = self.db.exec(db_qry.offset(offset).limit(limit)).all()
        pagination = Pagination(total_count=count_todos, current_page=page, limit=limit)

        return Routines, pagination

    def get_by_Routinename(self, Routinename: str) -> Optional[Routine]:
        return self.db.exec(select(Routine).where(Routine.name == Routinename)).one_or_none()

    def get_by_id(self, Routine_id: int) -> Optional[Routine]:
        return self.db.get(Routine, Routine_id)

    def get_all_Routines(self) -> list[Routine]:
        return self.db.exec(select(Routine)).all()

    def update_Routine(self, Routine_id:int, Routine_data: RoutineUpdate)->Routine:
        routine = self.db.get(Routine, Routine_id)
        if not routine:
            raise Exception("Invalid Routine id given")
        if Routine_data.name:
            routine.name = Routine_data.name
        if Routine_data.description:
            routine.description = Routine_data.description

        try:
            self.db.add(routine)
            self.db.commit()
            self.db.refresh(routine)
            return routine
        except Exception as e:
            logger.error(f"An error occurred while updating Routine: {e}")
            self.db.rollback()
            raise

    def delete_Routine(self, Routine_id: int):
        routine = self.db.get(Routine, Routine_id)
        if not routine:
            raise Exception("Routine doesn't exist")
        try:
            self.db.delete(routine)
            self.db.commit()
        except Exception as e:
            logger.error(f"An error occurred while deleting Routine: {e}")
            self.db.rollback()
            raise
