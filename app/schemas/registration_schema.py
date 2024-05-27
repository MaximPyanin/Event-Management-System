from pydantic import BaseModel

from app.constants.types import Types


class RegistrationDto(BaseModel):
    user_id: Types.uuid_pk
    event_id: Types.uuid_pk
