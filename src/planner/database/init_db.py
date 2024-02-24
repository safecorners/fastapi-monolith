from sqlalchemy.ext.asyncio import AsyncConnection

from planner.database import Base
from planner.models.events import Event  # noqa: F401
from planner.models.users import User  # noqa: F401


async def init_db(connection: AsyncConnection) -> None:
    await connection.run_sync(Base.metadata.drop_all)
    await connection.run_sync(Base.metadata.create_all)
