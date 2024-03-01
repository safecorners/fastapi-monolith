from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from application.database import Base

if TYPE_CHECKING:
    from application.models import User
    

class Event(Base):

    __tablename__ = "events"
 
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="events", foreign_keys=user_id)
    title: Mapped[str]
    image: Mapped[str]
    description: Mapped[str]
    tags: Mapped[List[str]] = mapped_column(type_=JSON)
    location: Mapped[str]

