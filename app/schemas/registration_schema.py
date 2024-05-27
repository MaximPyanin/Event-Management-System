from pydantic import BaseModel

from app.constants.types import Types


class RegistrationDto(BaseModel):
    user_id: Types.uuid_pk
    event_id: Types.uuid_pk
    # here only event id or user also supply ; when delete by registration id or by event and user id
