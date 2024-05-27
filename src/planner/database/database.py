import logging
from asyncio import current_task
from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from planner.database.orm import Base

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_url: str) -> None:
        # https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#using-multiple-asyncio-event-loops
        # TODO: We only use multiple event loops when testing, so we need to remove this smell.
        self._engine = create_async_engine(
            db_url,
            echo=True,
            poolclass=NullPool,
        )
        self._session_factory = async_scoped_session(
            async_sessionmaker(autocommit=False, autoflush=False, bind=self._engine),
            scopefunc=current_task,
        )

    async def create_database(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_database(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        session: AsyncSession = self._session_factory()
        try:
            yield session
        except Exception:
            logger.exception("Session rollback because of exception")
            await session.rollback()
            raise
        finally:
            await session.close()
