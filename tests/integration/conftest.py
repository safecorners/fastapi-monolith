from contextlib import contextmanager
from typing import Iterator

import pytest
from sqlalchemy import (
    create_engine,
    Engine,
    Connection,
    Transaction,
)
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from planner.database import Base, SessionFactory


@pytest.fixture
def test_db_url() -> str:
    return "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"


@pytest.fixture
def test_engine(test_db_url: str) -> Engine:
    test_engine = create_engine(url=test_db_url, echo=True)

    Base.metadata.drop_all(test_engine)
    Base.metadata.create_all(test_engine)

    return test_engine


@pytest.fixture(scope="function")
def transactional_session_factory(test_engine: Engine) -> SessionFactory:
    """
    https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites
    """

    @contextmanager
    def transactional_session_factory() -> Iterator[Session]:
        connection: Connection = test_engine.connect()
        transaction: Transaction = connection.begin()
        session_factory = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=connection,
                join_transaction_mode="create_savepoint",
            )
        )
        session: Session = session_factory()

        try:
            yield session
        finally:
            session.close()
            transaction.rollback()
            connection.close()

    return transactional_session_factory
