from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.constants.tags import Tags
from app.database.base import Base
from app.constants.types import Types

from app.database.models.feedback import Feedback

from app.database.models.tag import Tag
from app.database.models.user import User
from app.database.models.registration import Registration


class Event(Base):
    __tablename__ = "events"
    id: Mapped[Types.uuid_pk]
    location: Mapped[str]
    date: Mapped[datetime]
    created_at: Mapped[Types.created_at]
    description: Mapped[str]
    tag_id: Mapped[Tags] = mapped_column(ForeignKey("tags.id", ondelete="CASCADE"))
    organizer_id: Mapped[Types.uuid_pk] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )

    tag: Mapped["Tag"] = relationship(back_populates="events", uselist=False)
    organizer: Mapped["User"] = relationship(
        back_populates="organized_events", uselist=False
    )

    feedbacks: Mapped[list["Feedback"]] = relationship(
        back_populates="event", uselist=True
    )

    users: Mapped[list["User"]] = relationship(
        back_populates="events", uselist=True, secondary=Registration.__table__
    )

    __table_args__ = (CheckConstraint("date > CURRENT_TIMESTAMP"),)
