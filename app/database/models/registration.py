from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.constants.types import Types


class Registration(Base):
    __tablename__ = "registrations"
    id: Mapped[Types.UUID_PK]
    created_at: Mapped[Types.CREATED_AT]
    user_id: Mapped[Types.UUID_PK] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    event_id: Mapped[Types.UUID_PK] = mapped_column(
        ForeignKey("events.id", ondelete="CASCADE")
    )
