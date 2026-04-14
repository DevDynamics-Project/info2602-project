from fastapi import HTTPException
from app.dependencies.session import SessionDep
from app.dependencies.auth import AuthDep
from app.repositories.routine import RoutineRepository
from app.repositories.workout import WorkoutRepository
from app.services.routine_service import RoutineService
from app.schemas.routine import (
    RoutineCreate, RoutineResponse, AddWorkoutRequest,
    UpdateWorkoutInRoutineRequest, RemixWorkoutRequest
)
from app.schemas.workout import WorkoutResponse
from . import api_router


def _build_routine_response(routine, workouts_data: list) -> dict:
    return {
        "id": routine.id,
        "name": routine.name,
        "description": routine.description,
        "user_id": routine.user_id,
        "workouts": [
            {"workout": w["workout"], "sets": w["sets"], "reps": w["reps"], "order": w["order"]}
            for w in workouts_data
        ]
    }


@api_router.get("/routines", response_model=list[RoutineResponse])
async def list_routines(db: SessionDep, user: AuthDep):
    service = RoutineService(RoutineRepository(db))
    routines = service.get_user_routines(user.id)
    result = []
    for r in routines:
        workouts = RoutineRepository(db).get_workouts_for_routine(r.id)
        result.append(_build_routine_response(r, workouts))
    return result


@api_router.post("/routines", response_model=RoutineResponse, status_code=201)
async def create_routine(data: RoutineCreate, db: SessionDep, user: AuthDep):
    service = RoutineService(RoutineRepository(db))
    routine = service.create(data.name, data.description, user.id)
    return _build_routine_response(routine, [])


@api_router.get("/routines/{routine_id}", response_model=RoutineResponse)
async def get_routine(routine_id: int, db: SessionDep, user: AuthDep):
    service = RoutineService(RoutineRepository(db))
    try:
        data = service.get_full_routine(routine_id, user.id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Routine not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Forbidden")
    return _build_routine_response(data["routine"], data["workouts"])


@api_router.delete("/routines/{routine_id}", status_code=204)
async def delete_routine(routine_id: int, db: SessionDep, user: AuthDep):
    service = RoutineService(RoutineRepository(db))
    try:
        service.delete(routine_id, user.id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Routine not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Forbidden")


@api_router.patch("/routines/{routine_id}", response_model=RoutineResponse)
async def update_routine(routine_id: int, data: RoutineCreate, db: SessionDep, user: AuthDep):
    service = RoutineService(RoutineRepository(db))
    try:
        routine = service.update(routine_id, user.id, data.name, data.description)
    except ValueError:
        raise HTTPException(status_code=404, detail="Routine not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Forbidden")
    workouts = RoutineRepository(db).get_workouts_for_routine(routine_id)
    return _build_routine_response(routine, workouts)


@api_router.post("/routines/{routine_id}/workouts", response_model=RoutineResponse, status_code=201)
async def add_workout_to_routine(routine_id: int, data: AddWorkoutRequest, db: SessionDep, user: AuthDep):
    repo = RoutineRepository(db)
    service = RoutineService(repo)
    if not WorkoutRepository(db).get_by_id(data.workout_id):
        raise HTTPException(status_code=404, detail="Workout not found")
    try:
        service.add_workout(routine_id, user.id, data.workout_id, data.sets, data.reps, data.order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PermissionError:
        raise HTTPException(status_code=403, detail="Forbidden")
    full = service.get_full_routine(routine_id, user.id)
    return _build_routine_response(full["routine"], full["workouts"])


@api_router.delete("/routines/{routine_id}/workouts/{workout_id}", response_model=RoutineResponse)
async def remove_workout_from_routine(routine_id: int, workout_id: int, db: SessionDep, user: AuthDep):
    repo = RoutineRepository(db)
    service = RoutineService(repo)
    try:
        service.remove_workout(routine_id, user.id, workout_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Forbidden")
    full = service.get_full_routine(routine_id, user.id)
    return _build_routine_response(full["routine"], full["workouts"])


@api_router.patch("/routines/{routine_id}/workouts/{workout_id}", response_model=RoutineResponse)
async def update_workout_in_routine(
    routine_id: int, workout_id: int,
    data: UpdateWorkoutInRoutineRequest,
    db: SessionDep, user: AuthDep
):
    repo = RoutineRepository(db)
    service = RoutineService(repo)
    try:
        service.update_workout_in_routine(routine_id, user.id, workout_id, data.sets, data.reps, data.order)
    except ValueError:
        raise HTTPException(status_code=404, detail="Not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Forbidden")
    full = service.get_full_routine(routine_id, user.id)
    return _build_routine_response(full["routine"], full["workouts"])


@api_router.post("/routines/{routine_id}/workouts/{workout_id}/remix", response_model=RoutineResponse)
async def remix_workout_in_routine(
    routine_id: int, workout_id: int,
    data: RemixWorkoutRequest,
    db: SessionDep, user: AuthDep
):
    repo = RoutineRepository(db)
    service = RoutineService(repo)
    try:
        service.remix_workout(routine_id, user.id, workout_id, data.new_workout_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PermissionError:
        raise HTTPException(status_code=403, detail="Forbidden")
    full = service.get_full_routine(routine_id, user.id)
    return _build_routine_response(full["routine"], full["workouts"])


@api_router.get("/routines/{routine_id}/workouts/{workout_id}/alternatives", response_model=list[WorkoutResponse])
async def get_workout_alternatives(routine_id: int, workout_id: int, db: SessionDep, user: AuthDep):
    service = RoutineService(RoutineRepository(db))
    try:
        return service.get_alternatives(routine_id, user.id, workout_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Forbidden")
