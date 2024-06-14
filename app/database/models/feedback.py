import datetime

from sqlalchemy import ForeignKey, CheckConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.constants.types import Types
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.database.models.event import Event

from app.database.models.user import User


class Feedback(Base):
    __tablename__ = "feedbacks"
    id: Mapped[Types.UUID_PK]
    comment: Mapped[str]
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=datetime.datetime.utcnow,
    )
    rating: Mapped[float]
    event_id: Mapped[Types.UUID_PK] = mapped_column(
        ForeignKey("events.id", ondelete="CASCADE")
    )
    user_id: Mapped[Types.UUID_PK] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )

    event: Mapped["Event"] = relationship(back_populates="feedbacks", uselist=False)
    user: Mapped["User"] = relationship(back_populates="feedbacks", uselist=False)
    __table_args__ = (CheckConstraint("rating > 0 and rating <= 10 "),)
