from fastapi import Request, HTTPException, Query
from app.dependencies.session import SessionDep
from app.dependencies.auth import AuthDep
from app.repositories.workout import WorkoutRepository
from app.services.workout_service import WorkoutService
from app.schemas.workout import WorkoutResponse
from . import api_router


@api_router.get("/workouts", response_model=list[WorkoutResponse])
async def list_workouts(
    request: Request,
    db: SessionDep,
    user: AuthDep,
    q: str = Query(default="", description="Search query"),
):
    service = WorkoutService(WorkoutRepository(db))
    return service.search(q) if q else service.get_all()


@api_router.get("/workouts/{workout_id}", response_model=WorkoutResponse)
async def get_workout(workout_id: int, db: SessionDep, user: AuthDep):
    service = WorkoutService(WorkoutRepository(db))
    workout = service.get_by_id(workout_id)
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout
