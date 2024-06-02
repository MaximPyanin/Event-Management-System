from typing import Annotated

from pydantic import Field, BaseModel

from app.constants.types import Types


class FeedbackCreationDto(BaseModel):
    comment: str
    rating: Annotated[float, Field(gt=0, le=10)]
    event_id: Types.uuid_pk
    user_id: Types.uuid_pk


class FeedbackUpdateDto(BaseModel):
    comment: str
    rating: float
