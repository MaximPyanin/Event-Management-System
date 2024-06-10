from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base
from app.constants.roles import Roles
from typing import TYPE_CHECKING

if TYPE_CHECKING:
 from app.database.models.user import User


class Role(Base):
    __tablename__ = "roles"
    id: Mapped[Roles] = mapped_column(primary_key=True)
    users: Mapped[list["User"]] = relationship(back_populates="role", uselist=True)
