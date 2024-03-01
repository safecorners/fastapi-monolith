from dependency_injector import containers, providers

from application.config import Settings
from application.database import Database
from application.repositories import UserRepository
from application.services import UserService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["application.routers.user_router"])

    config = providers.Configuration()

    db = providers.Singleton(
        Database,
        db_url=config.postgres.url,
    )

    user_repository = providers.Factory(
        UserRepository,
        session_factory=db.provided.session,
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )


def create_container() -> containers.DeclarativeContainer:
    container = Container()
    settings = Settings()
    container.config.from_dict(settings.model_dump())

    return container
