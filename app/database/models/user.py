from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.database.base import Base
from app.constants.types import Types
from app.constants.roles import Roles
from app.database.models.event import Event
from app.database.models.feedback import Feedback
from app.database.models.registration import Registration
from app.database.models.role import Role


class User(Base):
    __tablename__ = "users"
    id: Mapped[Types.uuid_pk]
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    phone: Mapped[str]
    password: Mapped[bytes]
    role_id: Mapped[Roles] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"))

    role: Mapped["Role"] = relationship(back_populates="users", uselist=False)
    organized_events: Mapped[list["Event"]] = relationship(
        back_populates="organizer", uselist=True
    )
    feedbacks: Mapped[list["Feedback"]] = relationship(
        back_populates="user", uselist=True
    )
    events: Mapped[list["Event"]] = relationship(
        back_populates="users", uselist=True, secondary=Registration.__table__
    )
