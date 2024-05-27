from typing import Optional
from uuid import UUID

from sqlalchemy import ForeignKey, text, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.constants.tags import Tags
from app.database.base import Base
from app.constants.types import Types
from app.constants.roles import Roles
from app.database.models.event import Event
from app.database.models.role import Role
from app.database.models.tag import Tag
from app.database.models.user import User
from app.database.models.registration import Registration


class Feedback(Base):
    __table_name__ = "feedbacks"
    id: Mapped[Types.uuid_pk]
    comment: Mapped[str]
    rating: Mapped[float]
    event_id: Mapped[Types.uuid_pk] = mapped_column(
        ForeignKey("events.id", ondelete="CASCADE")
    )
    user_id: Mapped[Types.uuid_pk] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )

    event: Mapped["Event"] = relationship(back_populates="feedbacks", uselist=False)
    user: Mapped["User"] = relationship(back_populates="feedbacks", uselist=False)
    __table_args__ = (CheckConstraint("rating > 0 and rating <= 10 "),)
