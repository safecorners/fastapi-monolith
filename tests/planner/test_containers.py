import logging

from planner.containers import container

logger = logging.getLogger(__name__)


def test_configuration() -> None:
    logger.info(f"postgres_url={container.config.postgres.url()}")
