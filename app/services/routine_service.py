from app.repositories.routine import RoutineRepository
from app.models.routine import Routine
from app.models.workout import Workout
from typing import Optional


class RoutineService:
    def __init__(self, repo: RoutineRepository):
        self.repo = repo

    def create(self, name: str, description: str, user_id: int) -> Routine:
        return self.repo.create(name, description, user_id)

    def get_user_routines(self, user_id: int) -> list[Routine]:
        return self.repo.get_all_for_user(user_id)

    def get_by_id(self, routine_id: int) -> Optional[Routine]:
        return self.repo.get_by_id(routine_id)

    def delete(self, routine_id: int, user_id: int):
        routine = self.repo.get_by_id(routine_id)
        if not routine:
            raise ValueError("Routine not found")
        if routine.user_id != user_id:
            raise PermissionError("Not your routine")
        return self.repo.delete(routine_id)

    def update(self, routine_id: int, user_id: int, name: Optional[str] = None, description: Optional[str] = None):
        routine = self.repo.get_by_id(routine_id)
        if not routine:
            raise ValueError("Routine not found")
        if routine.user_id != user_id:
            raise PermissionError("Not your routine")
        return self.repo.update(routine_id, name, description)

    def add_workout(self, routine_id: int, user_id: int, workout_id: int, sets: int, reps: int, order: int):
        routine = self.repo.get_by_id(routine_id)
        if not routine:
            raise ValueError("Routine not found")
        if routine.user_id != user_id:
            raise PermissionError("Not your routine")
        return self.repo.add_workout(routine_id, workout_id, sets, reps, order)

    def remove_workout(self, routine_id: int, user_id: int, workout_id: int):
        routine = self.repo.get_by_id(routine_id)
        if not routine:
            raise ValueError("Routine not found")
        if routine.user_id != user_id:
            raise PermissionError("Not your routine")
        return self.repo.remove_workout(routine_id, workout_id)

    def update_workout_in_routine(self, routine_id: int, user_id: int, workout_id: int,
                                   sets: Optional[int], reps: Optional[int], order: Optional[int]):
        routine = self.repo.get_by_id(routine_id)
        if not routine:
            raise ValueError("Routine not found")
        if routine.user_id != user_id:
            raise PermissionError("Not your routine")
        return self.repo.update_workout_in_routine(routine_id, workout_id, sets, reps, order)

    def remix_workout(self, routine_id: int, user_id: int, old_workout_id: int, new_workout_id: int):
        routine = self.repo.get_by_id(routine_id)
        if not routine:
            raise ValueError("Routine not found")
        if routine.user_id != user_id:
            raise PermissionError("Not your routine")
        return self.repo.remix_workout(routine_id, old_workout_id, new_workout_id)

    def get_full_routine(self, routine_id: int, user_id: int) -> dict:
        routine = self.repo.get_by_id(routine_id)
        if not routine:
            raise ValueError("Routine not found")
        if routine.user_id != user_id:
            raise PermissionError("Not your routine")
        workouts = self.repo.get_workouts_for_routine(routine_id)
        return {"routine": routine, "workouts": workouts}

    def get_alternatives(self, routine_id: int, user_id: int, workout_id: int) -> list[Workout]:
        routine = self.repo.get_by_id(routine_id)
        if not routine:
            raise ValueError("Routine not found")
        if routine.user_id != user_id:
            raise PermissionError("Not your routine")
        return self.repo.get_alternatives(routine_id, workout_id)
