from fastapi import FastAPI

from planner.containers import create_container
from planner.routers import auth_router, event_router, user_router


def create_app() -> FastAPI:
    container = create_container()

    db = container.db()
    db.create_database()

    app = FastAPI()
    app.container = container  # type: ignore[attr-defined]

    app.include_router(user_router)
    app.include_router(event_router)
    app.include_router(auth_router)
    
    return app


app = create_app()
