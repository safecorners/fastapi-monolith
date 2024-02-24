from contextlib import asynccontextmanager
from typing import AsyncIterator, Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from planner.database import sessionmanager
from planner.database.init_db import init_db
from planner.routes.events import event_router
from planner.routes.users import user_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    async with sessionmanager.connect() as connection:
        await init_db(connection)
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan)

app.include_router(user_router, prefix="/users")
app.include_router(event_router, prefix="/events")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/status")
async def health_check() -> Dict[str, str]:
    return {"status": "ok"}
