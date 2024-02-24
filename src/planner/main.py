from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from planner.database.connection import conn
from planner.routes.events import event_router
from planner.routes.users import user_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    conn()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")


@app.get("/")
async def home() -> RedirectResponse:
    return RedirectResponse(url="/event/")
