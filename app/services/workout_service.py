from app.repositories.workout import WorkoutRepository
from app.models.workout import Workout, WorkoutBase
from typing import Optional


class WorkoutService:
    def __init__(self, repo: WorkoutRepository):
        self.repo = repo

    def get_all(self) -> list[Workout]:
        return self.repo.get_all()

    def get_by_id(self, workout_id: int) -> Optional[Workout]:
        return self.repo.get_by_id(workout_id)

    def search(self, query: str) -> list[Workout]:
        if not query:
            return self.repo.get_all()
        return self.repo.search(query)

    def create(self, data: WorkoutBase) -> Workout:
        return self.repo.create(data)
