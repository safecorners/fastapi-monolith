from typing import List

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from planner.database import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    title: Mapped[str]
    image: Mapped[str]
    description: Mapped[str]
    tags: Mapped[List[str]] = mapped_column(type_=JSON)
    location: str
