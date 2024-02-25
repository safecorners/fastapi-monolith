from pydantic import Field, PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="postgres_")

    host: str = Field(default="localhost")
    user: str = Field(default="postgres")
    password: str = Field(default="postgres")
    db: str = Field(default="postgres")
    port: str = Field(default="5432")

    @computed_field  # type: ignore[misc]
    @property
    def url(self) -> PostgresDsn:
        return PostgresDsn(
            f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
        )


class Settings(BaseSettings):
    db: BaseSettings = PostgresSettings()
