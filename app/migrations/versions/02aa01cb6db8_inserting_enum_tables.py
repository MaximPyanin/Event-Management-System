"""inserting enum tables

Revision ID: 02aa01cb6db8
Revises: 5952a83330ef
Create Date: 2024-06-08 23:03:19.657234

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "02aa01cb6db8"
down_revision: Union[str, None] = "5952a83330ef"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("INSERT INTO roles VALUES ('ADMIN'),('ORGANIZER'),('ATTENDEE')")
    op.execute("INSERT INTO tags VALUES ('FOOTBALL'),('BALLET'),('CONCERT')")


def downgrade() -> None:
    op.execute("DELETE FROM roles")
    op.execute("DELETE FROM tags")
