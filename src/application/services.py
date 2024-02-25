from typing import List
from uuid import uuid4

from application.models import User
from application.repositories import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    def get_users(self) -> List[User]:
        return self._user_repository.get_all()

    def get_user_by_id(self, user_id: int) -> User:
        return self._user_repository.get_by_id(user_id)

    def create_user(self) -> User:
        user_id = uuid4()
        return self._user_repository.add(email=f"{user_id}@email.com", password="pwd")

    def delete_user_by_id(self, user_id: int) -> None:
        return self._user_repository.delete_by_id(user_id)
