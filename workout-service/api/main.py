import sys

# databases is not actually used here, it's just an example client from FastAPI docs
# import databases
import uvicorn  # type: ignore
from fastapi import FastAPI
from fastapi.routing import APIRoute, APIRouter
from starlette.middleware.cors import CORSMiddleware

from api.application.health import health_handler
from api.application.workout_aggregate.workout_handler import WorkoutHandler
from api.domain.workout_aggregate.workout import Workout, WorkoutList
from api.domain.workout_aggregate.workout_repo import IWorkoutRepo
from api.domain.workout_aggregate.workout_service import WorkoutService
from api.infrastructure.workout_aggregate.workout_repo import StubWorkoutRepo

# inject database connection info from config here
# and use it to connect to some database client like:
# pg_client = databases.Database(DATABASE_URL)
# then inject it into your repo implementation like
# entity_repo: WorkoutRepo = PGWorkoutRepo(pg_client=pgclient)
workout_repo: IWorkoutRepo = StubWorkoutRepo()
workout_service = WorkoutService(repo=workout_repo)
workout_handler = WorkoutHandler(service=workout_service)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

get_service_health_route = APIRoute(
    path="/healthz",
    endpoint=health_handler.get_service_health,
    methods=["GET"],
    name="Get Service Health",
)
health_router = APIRouter(routes=[get_service_health_route])
app.include_router(health_router)


API_PREFIX_V0 = "/api/v0"
API_V0_WORKOUTS_PATH = API_PREFIX_V0 + "/workouts"
API_V0_WORKOUTS_ID_PATH = API_PREFIX_V0 + "/workouts/{workouts_id}"

# FastAPI does not yet support introspection on class-based handlers.
# Using APIRoute/APIRouter instead of decorators allows our handlers to be
# members of a class, which allows us to inject the Service as a dependency.
# The cost is some extra boilerplate config like declaring the response model,
# instead of the magic/introspection provided by the decorators.
get_workout_route = APIRoute(
    path=API_V0_WORKOUTS_ID_PATH,
    endpoint=workout_handler.get,
    methods=["GET"],
    response_model=Workout,
    name="Get Workout",
)
list_workouts_route = APIRoute(
    path=API_V0_WORKOUTS_PATH,
    endpoint=workout_handler.list,
    methods=["GET"],
    response_model=WorkoutList,
    name="List Workouts",
)
workout_router = APIRouter(
    routes=[
        get_workout_route,
        list_workouts_route,
    ]
)
app.include_router(workout_router)


# Apply these startup and shutdown signal handlers
# to whichever database client/engine you use

# @app.on_event("startup")
# async def startup():
#     await database.connect()
#
#
# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()


def main():  # pylint: disable=missing-function-docstring
    uvicorn.run("api.main:app", host="0.0.0.0", port=8080)


if __name__ == "__main__":
    sys.exit(main())
