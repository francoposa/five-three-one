from typing import AsyncGenerator

import sqlalchemy as sa
from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker

from api.infrastructure.user_aggregate.user_repo import UserDB

DB_METADATA = sa.MetaData()
User_DB_Declarative_Meta: DeclarativeMeta = declarative_base(metadata=DB_METADATA)

DATABASE_URL = "postgresql+asyncpg://postgres@localhost:5432/531_user"
engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class UserTable(User_DB_Declarative_Meta, SQLAlchemyBaseUserTable):
    pass


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(UserDB, session, UserTable)
