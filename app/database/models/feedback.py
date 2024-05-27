from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.constants.types import Types

from app.database.models.event import Event

from app.database.models.user import User


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
