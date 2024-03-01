from fastapi import FastAPI

from application.containers import create_container
from application.routers import user_router


def create_app() -> FastAPI:
    container = create_container()

    db = container.db()
    db.create_database()

    app = FastAPI()
    app.container = container
    app.include_router(user_router)
    return app


app = create_app()
