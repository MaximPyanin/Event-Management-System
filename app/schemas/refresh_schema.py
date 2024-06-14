from uuid import UUID

from pydantic import BaseModel


class RefreshToken(BaseModel):
    refresh_token: UUID
