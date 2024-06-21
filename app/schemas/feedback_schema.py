from typing import Annotated

from pydantic import Field, BaseModel

from app.constants.types import Types


class FeedbackCreationDto(BaseModel):
    comment: str
    rating: Annotated[float, Field(gt=0, le=10)]
    event_id: Types.UUID_PK
    user_id: Types.UUID_PK


class FeedbackUpdateDto(BaseModel):
    comment: str
    rating: float
