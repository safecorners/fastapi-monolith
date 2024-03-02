from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from planner.application import create_app


@pytest.fixture()
def app() -> Generator[FastAPI, None, None]:
    app = create_app()
    yield app


@pytest.fixture()
def client(app: FastAPI) -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client
