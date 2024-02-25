import logging

from application.containers import create_container

logger = logging.getLogger(__name__)


def test_configuration() -> None:
    container = create_container()

    logger.info(f"postgres_url={container.config.postgres.url()}")
