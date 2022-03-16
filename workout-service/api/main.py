import sys

# databases is not actually used here, it's just an example client from FastAPI docs
# import databases
import uvicorn  # type: ignore
from fastapi import FastAPI
from fastapi.routing import APIRoute, APIRouter
from sqlalchemy.ext.asyncio import create_async_engine
from starlette.middleware.cors import CORSMiddleware

from api.application.health import health_handler
from api.application.workout_aggregate.workout_handler import WorkoutHandler
from api.domain.workout_aggregate.workout import Workout, WorkoutList
from api.domain.workout_aggregate.workout_repo import IWorkoutRepo
from api.domain.workout_aggregate.workout_service import WorkoutService
from api.infrastructure.datastore.postgres.tables import get_user_db
from api.infrastructure.user_aggregate.user_repo import (
    User,
    UserCreate,
    UserDB,
    UserUpdate,
)
from api.infrastructure.workout_aggregate.workout_repo import StubWorkoutRepo

# inject database connection info from config here
# and use it to connect to some database client like:
# pg_client = databases.Database(DATABASE_URL)
# then inject it into your repo implementation like
# entity_repo: WorkoutRepo = PGWorkoutRepo(pg_client=pgclient)
engine = create_async_engine("postgresql+asyncpg://postgres@localhost:5432/five_three_one")
workout_repo: IWorkoutRepo = StubWorkoutRepo()
workout_service = WorkoutService(repo=workout_repo)
workout_handler = WorkoutHandler(service=workout_service)


from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)

SECRET = "SECRET"

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager

SECRET = "SECRET"


class UserManager(BaseUserManager[UserCreate, UserDB]):
    user_db_model = UserDB
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: UserDB, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: UserDB, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: UserDB, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


from fastapi_users import FastAPIUsers

fastapi_users = FastAPIUsers(
    get_user_manager,
    [auth_backend],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

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

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(),
    prefix="/auth",
    tags=["auth"],
)


@app.get("/protected-route")
def protected_route(user: User = Depends(fastapi_users.current_user())):
    return f"Hello, {user.email}. You are authenticated with a cookie or a JWT."


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
