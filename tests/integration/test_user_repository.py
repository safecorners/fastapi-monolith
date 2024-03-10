import pytest


from planner.repositories.user_repository import UserRepository
from planner.database import SessionFactory


@pytest.fixture
def user_repository(transactional_session_factory: SessionFactory) -> UserRepository:
    return UserRepository(session_factory=transactional_session_factory)


def test_create_user(user_repository: UserRepository) -> None:
    email = "test@example.com"
    password = "password"
    is_active = True
    user = user_repository.add(email=email, password=password, is_active=is_active)

    assert user.email == email
    assert user.hashed_password == password
    assert user.is_active == is_active
