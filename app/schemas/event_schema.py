import uuid
from datetime import date, datetime


from pydantic import BaseModel, field_validator


from app.constants.event_tags import EventTags


class EventCreationDto(BaseModel):
    location: str
    date: date
    description: str
    tag: EventTags
    organizer_id: uuid.UUID

    @field_validator("date")
    @classmethod
    def date_check(cls, v: date):
        if v < datetime.utcnow().date():
            raise ValueError("date must be in future")
        return v


class EventUpdateDto(BaseModel):
    description: str
