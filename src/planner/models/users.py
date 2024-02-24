from typing import List, Optional

from sqlalchemy.orm import Mapped, mapped_column

from planner.database import Base
from planner.models.events import Event


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    email: Mapped[str] = mapped_column(index=True)
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    events: Mapped[Optional[List[Event]]] = mapped_column(default=None)
