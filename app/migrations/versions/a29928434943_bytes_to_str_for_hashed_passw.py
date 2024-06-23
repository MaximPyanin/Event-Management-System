"""bytes to str for hashed passw

Revision ID: a29928434943
Revises: c35324722457
Create Date: 2024-06-23 00:41:12.094874

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "a29928434943"
down_revision: Union[str, None] = "c35324722457"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TABLE users ADD COLUMN password_text TEXT")
    op.execute("UPDATE users SET password_text = encode(password, 'escape')")
    op.execute("ALTER TABLE users DROP COLUMN password")
    op.execute("ALTER TABLE users RENAME COLUMN password_text TO password")


def downgrade() -> None:
    op.execute("ALTER TABLE users ADD COLUMN password_bytea BYTEA")
    op.execute("UPDATE users SET password_bytea = decode(password, 'escape')")
    op.execute("ALTER TABLE users DROP COLUMN password")
    op.execute("ALTER TABLE users RENAME COLUMN password_bytea TO password")
