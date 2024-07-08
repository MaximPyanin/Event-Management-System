from pydantic import BaseModel

from app.constants.types import Types


class RegistrationDto(BaseModel):
    user_id: Types.UUID_PK
    event_id: Types.UUID_PK
