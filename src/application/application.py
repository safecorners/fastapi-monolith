from typing import Dict

from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI()

    @app.get("/")
    def hello_world() -> Dict[str, str]:
        return {"message": "Hello, World!"}

    @app.get("/health")
    async def health_check() -> Dict[str, str]:
        return {"message": "ok"}

    return app
