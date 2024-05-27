from typing import Optional
from uuid import UUID

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.constants.tags import Tags
from app.database.base import Base
from app.constants.types import Types
from app.constants.roles import Roles
from app.database.models.role import Role
from app.database.models.tag import Tag


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
