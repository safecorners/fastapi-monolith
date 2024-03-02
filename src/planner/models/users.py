from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from planner.database import Base

if TYPE_CHECKING:
    from planner.models import Event


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    events: Mapped[List["Event"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return (
            f"<User(id={self.id}, "
            f'email="{self.email}", '
            f'hashed_password="{self.hashed_password}", '
            f"is_active={self.is_active})>"
        )
