import pydantic
from fastapi import HTTPException

from api.domain.workout_aggregate.workout import Workout, WorkoutList
from api.domain.workout_aggregate.workout_errors import WorkoutNotFoundError
from api.domain.workout_aggregate.workout_service import WorkoutService


class WorkoutHandler:
    def __init__(self, service: WorkoutService):
        self._service = service

    async def get(self, workout_id: pydantic.UUID4) -> Workout:
        try:
            return await self._service.get(workout_id)
        except WorkoutNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e

    async def list(self, page: int = 0, size: int = 20) -> WorkoutList:
        return await self._service.list(page=page, size=size)
