from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from planner.containers import container
from planner.routers import auth_router, event_router, user_router


@asynccontextmanager
async def lifepsan(app: FastAPI) -> AsyncIterator[None]:
    print("lifespan:startup")
    db = container.db()
    await db.drop_database()
    await db.create_database()

    yield
    print("lifespan:shutdown")


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifepsan)

    app.container = container  # type: ignore[attr-defined]

    app.include_router(user_router)
    app.include_router(event_router)
    app.include_router(auth_router)

    return app


app = create_app()
