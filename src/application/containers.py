from dependency_injector import containers, providers

from application.config import Settings


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()


def create_container() -> containers.DeclarativeContainer:
    container = Container()
    settings = Settings()
    container.config.from_dict(settings.model_dump())

    return container
