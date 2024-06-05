import uuid
from datetime import date, datetime


from pydantic import BaseModel, field_validator


from app.constants.tags import Tags


class EventCreationDto(BaseModel):
    location: str
    date: date
    description: str
    tag: Tags
    organizer_id: uuid.UUID

    @field_validator("date")
    @classmethod
    def date_check(cls, v: date):
        if v <= datetime.now().date():
            raise ValueError("date must be in future")
        return v


class EventUpdateDto(BaseModel):
    description: str
