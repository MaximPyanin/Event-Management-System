from datetime import datetime
from typing import Annotated
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.orm import mapped_column


class Types:
    UUID_PK = Annotated[
        UUID, mapped_column(primary_key=True, server_default=text("gen_random_uuid()"))
    ]
    CREATED_AT = Annotated[
        datetime,
        mapped_column(server_default=text("CURRENT_TIMESTAMP")),
    ]
