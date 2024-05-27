import uuid
from datetime import datetime


from pydantic import BaseModel, field_validator


from app.constants.tags import Tags


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
