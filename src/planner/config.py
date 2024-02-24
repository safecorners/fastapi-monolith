from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    db_url: str = (
        "postgresql+asyncpg://planner-dev:planner-dev@localhost:5432/planner-dev"
    )
    echo: bool = True
