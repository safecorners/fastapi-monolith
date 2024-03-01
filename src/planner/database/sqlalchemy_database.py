import contextlib
from typing import AsyncIterator, Optional

from sqlalchemy.ext.asyncio import (AsyncConnection, AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.orm import declarative_base
from typing_extensions import Unpack

from planner.config import DatabaseSettings

Base = declarative_base()


class SQLAlchemyDatabase:
    def __init__(self, db_url: str, **kwargs: Unpack[...]) -> None:
        self._engine: Optional[AsyncEngine] = create_async_engine(db_url, **kwargs)
        self._sessionmaker: Optional[
            async_sessionmaker[AsyncSession]
        ] = async_sessionmaker(autocommit=False, bind=self._engine)

    async def close(self) -> None:
        if self._engine is None:
            raise Exception("Database is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("Database is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("Database is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


database_settings = DatabaseSettings()

sessionmanager = SQLAlchemyDatabase(
    database_settings.db_url,
    echo=database_settings.echo,
)


async def get_db_session() -> AsyncSession:
    async with sessionmanager.session() as session:
        yield session
        yield session
