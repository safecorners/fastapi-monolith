from typing import List
from uuid import uuid4

from planner.auth import HashPassword, JWTHandler
from planner.exceptions import DuplicatedError, InvalidUsernameOrPasswordError
from planner.models import User
from planner.repositories import UserRepository
from planner.schemas.token import Token


class UserService:    
    def __init__(self, user_repository: UserRepository, hash_password: HashPassword, jwt_handler:JWTHandler) -> None:
        self._user_repository = user_repository
        self._hash_password = hash_password
        self._jwt_handler = jwt_handler

    def get_users(self) -> List[User]:
        return self._user_repository.get_all()

    def get_user_by_id(self, user_id: int) -> User:
        return self._user_repository.get_by_id(user_id)

    def create_user(self) -> User:
        user_id = uuid4()
        return self._user_repository.add(email=f"{user_id}@email.com", password="pwd")

    def delete_user_by_id(self, user_id: int) -> None:
        return self._user_repository.delete_by_id(user_id)

    def sign_up(self, email: str, password: str) -> None:
        user_exist = self._user_repository.get_by_email(email)
        if user_exist:
            raise DuplicatedError()
        
        hashed_password = self._hash_password.create_hash(password)
        self._user_repository.add(email, hashed_password, is_active=True)

    def sign_in(self, email: str, password: str) -> Token:
        user_exist = self._user_repository.get_by_email(email)
        if not user_exist:
            raise InvalidUsernameOrPasswordError()
        
        if self._hash_password.verify_hash(password, user_exist.hashed_password):
            access_token = self._jwt_handler.create_access_token(user_exist.email)
            return Token(access_token=access_token, token_type="Bearer",)

        raise InvalidUsernameOrPasswordError()
       