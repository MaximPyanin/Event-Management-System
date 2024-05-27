from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.constants.types import Types


class Registration(Base):
    __tablename__ = "registrations"
    id: Mapped[Types.uuid_pk]
    created_at: Mapped[Types.created_at]
    user_id: Mapped[Types.uuid_pk] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    event_id: Mapped[Types.uuid_pk] = mapped_column(
        ForeignKey("events.id", ondelete="CASCADE")
    )
