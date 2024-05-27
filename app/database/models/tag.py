from typing import Optional
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.database.base import Base
from app.constants.types import Types
from app.constants.roles import Roles
from app.database.models.role import Role
from app.constants.tags import Tags
from app.database.models.event import Event


class Tag(Base):
    __tablename__ = "tags"
    id: Mapped[Tags] = mapped_column(primary_key=True)
    events: Mapped[list["Event"]] = relationship(back_populates="tag", uselist=True)
