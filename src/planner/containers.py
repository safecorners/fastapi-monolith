from dependency_injector import containers, providers

from planner.auth import HashPassword, JWTHandler
from planner.config import Settings
from planner.database import Database
from planner.repositories import EventRepository, UserRepository
from planner.services import EventService, UserService


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(
        modules=[
            "planner.routers.user_router",
            "planner.routers.event_router",
            "planner.auth.authenticate"
        ]
    )

    config = providers.Configuration()

    db = providers.Singleton(
        Database,
        db_url=config.postgres.url,
    )

    hash_password = providers.Factory(HashPassword)

    jwt_handler = providers.Factory(JWTHandler, secret_key=config.jwt.secret_key)

    user_repository = providers.Factory(
        UserRepository,
        session_factory=db.provided.session,
    )

    event_repository = providers.Factory(
        EventRepository,
        session_factory=db.provided.session,
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
        hash_password=hash_password,
        jwt_handler=jwt_handler,
    )

    event_service = providers.Factory(EventService, event_repository=event_repository)


def create_container() -> Container:
    container = Container()
    settings = Settings()
    container.config.from_dict(settings.model_dump())

    return container
