import logging
from asyncio import current_task
from contextlib import AbstractContextManager, asynccontextmanager
from typing import Callable

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    ...


class Database:
    def __init__(self, db_url: str) -> None:
        self._engine = create_async_engine(db_url, echo=True)
        self._session_factory = async_scoped_session(
            async_sessionmaker(autocommit=False, autoflush=False, bind=self._engine),
            scopefunc=current_task,
        )

    async def create_database(self) -> None:
        async with self._engine.connect() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @asynccontextmanager
    async def session(self) -> Callable[..., AbstractContextManager[AsyncSession]]:
        # TODO:https://github.com/python/mypy/issues/16260
        session: AsyncSession = self._session_factory()
        try:
            yield session
        except Exception:
            logger.exception("Session rollback because of exception")
            await session.rollback()
            raise
        finally:
            await session.close()
