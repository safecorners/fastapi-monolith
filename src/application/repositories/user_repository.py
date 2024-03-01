from contextlib import AbstractContextManager
from typing import Callable, List, Optional

from sqlalchemy.orm import Session

from application.exceptions import UserNotFoundError
from application.models import User


class UserRepository:
    def __init__(
        self, session_factory: Callable[..., AbstractContextManager[Session]]
    ) -> None:
        self.session_factory = session_factory

    def get_all(self) -> List[User]:
        with self.session_factory() as session:
            return session.query(User).all()

    def get_by_id(self, user_id: int) -> User:
        with self.session_factory() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                raise UserNotFoundError(user_id)
            return user

    def add(self, email: str, password: str, is_active: bool = True) -> User:
        with self.session_factory() as session:
            user = User(email=email, hashed_password=password, is_active=is_active)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    def delete_by_id(self, user_id: int) -> None:
        with self.session_factory() as session:
            entity: Optional[User] = (
                session.query(User).filter(User.id == user_id).first()
            )
            if not entity:
                raise UserNotFoundError(user_id)
            session.delete(entity)
            session.commit()
