from datetime import datetime
from enum import Enum
from typing import Annotated
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.orm import mapped_column


class Types(Enum):
    uuid_pk = Annotated[
        UUID, mapped_column(primary_key=True, server_default=text("gen_random_uuid()"))
    ]
    created_at: Annotated[
        datetime, mapped_column(server_default=text("CURRENT_TIMESTAMP AT TIME ZONE 'UTC' "))
    ]
