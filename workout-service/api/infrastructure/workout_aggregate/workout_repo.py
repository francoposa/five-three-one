import pydantic

from api.domain.workout_aggregate.workout import Workout, WorkoutList
from api.domain.workout_aggregate.workout_repo import IWorkoutRepo


class StubWorkoutRepo(IWorkoutRepo):
    async def get(self, workout_id: pydantic.UUID4) -> Workout:
        pass

    async def list(self, page: int = 0, size: int = 0) -> WorkoutList:
        pass

    async def create(self, workout: Workout) -> Workout:
        pass

    async def update(self, workout: Workout) -> Workout:
        pass

    async def create_or_update(self, workout: Workout) -> Workout:
        pass

    async def delete(self, workout_id: pydantic.UUID4) -> Workout:
        pass
