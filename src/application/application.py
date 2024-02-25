from fastapi import FastAPI

from application import endpoints
from application.containers import create_container


def create_app() -> FastAPI:
    container = create_container()

    db = container.db()
    db.create_database()

    app = FastAPI()
    app.container = container
    app.include_router(endpoints.router)
    return app


app = create_app()
