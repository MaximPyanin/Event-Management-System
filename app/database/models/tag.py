from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.constants.tags import Tags
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.database.models.event import Event


class Tag(Base):
    __tablename__ = "tags"
    id: Mapped[Tags] = mapped_column(primary_key=True)
    events: Mapped[list["Event"]] = relationship(back_populates="tag", uselist=True)
