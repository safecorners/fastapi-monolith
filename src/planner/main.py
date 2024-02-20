from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from planner.database.connection import Settings
from planner.routes.events import event_router
from planner.routes.users import user_router

app = FastAPI()
settings = Settings()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")


@app.on_event("startup")
async def init_db() -> None:
    await settings.initialize_database()
