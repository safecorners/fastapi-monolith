import logging

from planner.containers import Container, create_container

logger = logging.getLogger(__name__)


def test_configuration() -> None:
    container: Container = create_container()

    logger.info(f"postgres_url={container.config.postgres.url()}")
