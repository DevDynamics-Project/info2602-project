from sqlmodel import Session, select
from app.models.routine import Routine
from app.models.workout_routine import RoutineWorkout
from app.models.workout import Workout
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class RoutineRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, description: str, user_id: int) -> Routine:
        try:
            routine = Routine(name=name, description=description, user_id=user_id)
            self.db.add(routine)
            self.db.commit()
            self.db.refresh(routine)
            return routine
        except Exception as e:
            logger.error(f"Error creating routine: {e}")
            self.db.rollback()
            raise

    def get_by_id(self, routine_id: int) -> Optional[Routine]:
        return self.db.get(Routine, routine_id)

    def get_all_for_user(self, user_id: int) -> list[Routine]:
        return self.db.exec(
            select(Routine).where(Routine.user_id == user_id)
        ).all()

    def delete(self, routine_id: int) -> Optional[Routine]:
        routine = self.db.get(Routine, routine_id)
        if not routine:
            return None
        links = self.db.exec(
            select(RoutineWorkout).where(RoutineWorkout.routine_id == routine_id)
        ).all()
        for link in links:
            self.db.delete(link)
        self.db.delete(routine)
        self.db.commit()
        return routine

    def update(self, routine_id: int, name: Optional[str] = None, description: Optional[str] = None) -> Optional[Routine]:
        routine = self.db.get(Routine, routine_id)
        if not routine:
            return None
        if name:
            routine.name = name
        if description is not None:
            routine.description = description
        self.db.add(routine)
        self.db.commit()
        self.db.refresh(routine)
        return routine

    def add_workout(self, routine_id: int, workout_id: int, sets: int = 3, reps: int = 10, order: int = 0) -> RoutineWorkout:
        existing = self.db.exec(
            select(RoutineWorkout).where(
                RoutineWorkout.routine_id == routine_id,
                RoutineWorkout.workout_id == workout_id
            )
        ).first()
        if existing:
            raise ValueError("Workout already in routine")
        link = RoutineWorkout(
            routine_id=routine_id,
            workout_id=workout_id,
            sets=sets,
            reps=reps,
            order=order
        )
        self.db.add(link)
        self.db.commit()
        self.db.refresh(link)
        return link

    def remove_workout(self, routine_id: int, workout_id: int) -> Optional[RoutineWorkout]:
        link = self.db.exec(
            select(RoutineWorkout).where(
                RoutineWorkout.routine_id == routine_id,
                RoutineWorkout.workout_id == workout_id
            )
        ).first()
        if not link:
            return None
        self.db.delete(link)
        self.db.commit()
        return link

    def update_workout_in_routine(self, routine_id: int, workout_id: int,
                                   sets: Optional[int] = None,
                                   reps: Optional[int] = None,
                                   order: Optional[int] = None) -> Optional[RoutineWorkout]:
        link = self.db.exec(
            select(RoutineWorkout).where(
                RoutineWorkout.routine_id == routine_id,
                RoutineWorkout.workout_id == workout_id
            )
        ).first()
        if not link:
            return None
        if sets is not None:
            link.sets = sets
        if reps is not None:
            link.reps = reps
        if order is not None:
            link.order = order
        self.db.add(link)
        self.db.commit()
        self.db.refresh(link)
        return link

    def remix_workout(self, routine_id: int, old_workout_id: int, new_workout_id: int) -> RoutineWorkout:
        link = self.db.exec(
            select(RoutineWorkout).where(
                RoutineWorkout.routine_id == routine_id,
                RoutineWorkout.workout_id == old_workout_id
            )
        ).first()
        if not link:
            raise ValueError("Workout not found in routine")
        already = self.db.exec(
            select(RoutineWorkout).where(
                RoutineWorkout.routine_id == routine_id,
                RoutineWorkout.workout_id == new_workout_id
            )
        ).first()
        if already:
            raise ValueError("Replacement workout already in routine")
        old_sets, old_reps, old_order = link.sets, link.reps, link.order
        self.db.delete(link)
        self.db.flush()
        new_link = RoutineWorkout(
            routine_id=routine_id,
            workout_id=new_workout_id,
            sets=old_sets,
            reps=old_reps,
            order=old_order
        )
        self.db.add(new_link)
        self.db.commit()
        self.db.refresh(new_link)
        return new_link

    def get_workouts_for_routine(self, routine_id: int) -> list[dict]:
        links = self.db.exec(
            select(RoutineWorkout).where(RoutineWorkout.routine_id == routine_id)
        ).all()
        result = []
        for link in sorted(links, key=lambda x: x.order):
            workout = self.db.get(Workout, link.workout_id)
            if workout:
                result.append({
                    "workout": workout,
                    "sets": link.sets,
                    "reps": link.reps,
                    "order": link.order
                })
        return result

    def get_alternatives(self, routine_id: int, workout_id: int) -> list[Workout]:
        source = self.db.get(Workout, workout_id)
        if not source:
            return []
        links = self.db.exec(
            select(RoutineWorkout).where(RoutineWorkout.routine_id == routine_id)
        ).all()
        in_routine_ids = {l.workout_id for l in links}
        candidates = self.db.exec(
            select(Workout).where(
                (Workout.muscle_group == source.muscle_group) |
                (Workout.difficulty == source.difficulty)
            )
        ).all()
        return [w for w in candidates if w.id not in in_routine_ids and w.id != workout_id]
