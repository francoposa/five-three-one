import uuid
from abc import ABC, abstractmethod

from api.domain.workout_aggregate.workout import Workout, WorkoutList


class IWorkoutRepo(ABC):
    """IEntityRepo defines the interface for Repository implementations providing
    Create-Read-Update-Delete operations for the Entity domain aggregate root

    Implement this interface to provide CRUD access to object storage
    where the interface methods are appropriate, such as a REST API,
    relational/document DB, file system, in-memory map/tree, etc.

    Repository implementation code does NOT contain business logic!
    Repository *implementations* are an infrastructure-layer construct.
    A Repository implementation's purpose is to provide an implementation-agnostic interface
    to the domain layer, encapsulating the details of interacting with the underlying datastore.

    Without applying a Unit of Work or similar pattern, multiple calls to methods of
    a Repository implementation are not assumed to be ACID-transactional.
    """

    @abstractmethod
    async def get(self, workout_id: uuid.UUID) -> Workout:
        pass

    @abstractmethod
    async def list(self, page: int = 0, size: int = 0) -> WorkoutList:
        pass

    @abstractmethod
    async def create(self, workout: Workout) -> Workout:
        pass

    @abstractmethod
    async def update(self, workout: Workout) -> Workout:
        pass

    @abstractmethod
    async def create_or_update(self, workout: Workout) -> Workout:
        pass

    @abstractmethod
    async def delete(self, workout_id: uuid.UUID) -> Workout:
        pass
