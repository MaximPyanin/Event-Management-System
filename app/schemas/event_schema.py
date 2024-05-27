import uuid
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, field_validator
from pydantic import EmailStr
from app.constants.roles import Roles
from pydantic import Field

from app.constants.tags import Tags
from app.constants.types import Types


class EventCreationDto(BaseModel):
    location: str
    date: datetime
    description: str
    tag: Tags
    organizer_id: uuid.UUID

    @field_validator("date")
    @classmethod
    def date_check(cls, v: datetime):
        if v <= datetime.now():
            raise ValueError("date must be in the future")
        return v


class EventUpdateDto(BaseModel):
    description: str
    # all nust be or predefined


print(EventUpdateDto(description=""), EventUpdateDto(description="").model_dump())
