"""add admin user

Revision ID: 864b70d79a93
Revises: 02aa01cb6db8
Create Date: 2024-06-08 23:18:09.500947

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from app.services.config_service import AppConfig
# revision identifiers, used by Alembic.
revision: str = "864b70d79a93"
down_revision: Union[str, None] = "02aa01cb6db8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(f"INSERT INTO users(username,email,phone,password,role_id) VALUES ('admin',{AppConfig.DOMAIN},{AppConfig.DOMAIN},)")

def downgrade() -> None:
    pass
