import logging
from typing import List, Optional

from sqlalchemy import select

from planner.database import SessionFactory
from planner.exceptions import UserNotFoundError
from planner.models import User

logger = logging.getLogger(__name__)


class UserRepository:
    def __init__(self, session_factory: SessionFactory) -> None:
        self.session_factory = session_factory

    async def get_all(self) -> List[User]:
        logger.info("I Have Not Mocked!")
        async with self.session_factory() as session:
            stmt = select(User)
            result = await session.execute(stmt)
            users = list(result.scalars().all())
            return users

    async def get_by_id(self, user_id: int) -> User:
        async with self.session_factory() as session:
            stmt = select(User).where(User.id == user_id)
            result = await session.execute(stmt)
            user = result.scalars().first()
            if user is None:
                raise UserNotFoundError(user_id)
            return user

    async def get_by_email(self, email: str) -> Optional[User]:
        async with self.session_factory() as session:
            stmt = select(User).where(User.email == email)
            result = await session.execute(stmt)
            user = result.scalars().first()
            return user

    async def add(self, email: str, password: str, is_active: bool = True) -> User:
        async with self.session_factory() as session:
            user = User(email=email, hashed_password=password, is_active=is_active)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    async def delete_by_id(self, user_id: int) -> None:
        async with self.session_factory() as session:
            stmt = select(User).where(User.id == user_id)
            result = await session.execute(stmt)
            user = result.scalars().first()
            if user is None:
                raise UserNotFoundError(user_id)
            await session.delete(user)
            await session.commit()
