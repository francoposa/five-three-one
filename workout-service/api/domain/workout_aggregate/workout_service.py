import uuid

from api.domain.workout_aggregate.workout import Workout, WorkoutList
from api.domain.workout_aggregate.workout_repo import IWorkoutRepo


class WorkoutService:
    """EntityService encapsulates all Entity aggregate root domain logic and provides
    an interface for all other components to interact with the Entity aggregate root.

    EntityService is an example implementation of the Service pattern

    * All operations performed by an API endpoint, user interface, message queue handler,
        or otherwise should be done using the public EntityService interface.
    * Services contain only "business"/domain logic or abstractions of underlying infrastructure
        concepts, such as the "Unit of Work" pattern as an abstraction of database transactions.
    * Services wrap around Repository implementations and should call the public methods of a
        Repository in order to persist any changes to application state
    * Services do not perform the Repository's role of interacting with the infrastructure layer
    """

    def __init__(self, repo: IWorkoutRepo):
        self._repo = repo

    async def get(self, workout_id: uuid.UUID) -> Workout:
        pass

    async def list(self, page: int = 0, size: int = 0) -> WorkoutList:
        pass

    async def create(self, workout: Workout) -> Workout:
        pass

    async def update(self, workout: Workout) -> Workout:
        pass

    async def create_or_update(self, workout: Workout) -> Workout:
        pass

    async def delete(self, workout_id: uuid.UUID) -> Workout:
        pass
