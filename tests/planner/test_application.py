from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import AsyncClient
from planner.application import create_app


@pytest.fixture()
def app() -> Generator[FastAPI, None, None]:
    app = create_app()
    yield app


@pytest.fixture()
def client(app: FastAPI) -> Generator[AsyncClient, None, None]:
    with AsyncClient(app) as client:
        yield client
