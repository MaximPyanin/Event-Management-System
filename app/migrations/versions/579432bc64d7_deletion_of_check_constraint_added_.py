"""deletion of check constraint ,added check trigger

Revision ID: 579432bc64d7
Revises: a29928434943
Create Date: 2024-06-24 19:42:46.299391

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "579432bc64d7"
down_revision: Union[str, None] = "a29928434943"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TABLE events DROP constraint events_date_check")
    op.execute("""
    CREATE OR REPLACE FUNCTION check_date_on_insert()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        IF NEW.date < CURRENT_DATE THEN
            RAISE EXCEPTION 'Date must be greater than or equal to current date';
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

    """)
    op.execute("""
    CREATE TRIGGER check_date_before_insert
BEFORE INSERT ON events
FOR EACH ROW
EXECUTE FUNCTION check_date_on_insert();
    """)


def downgrade() -> None:
    op.execute(
        "ALTER TABLE events ADD CONSTRAINT events_date_check CHECK ( date >= CURRENT_DATE )"
    )
    op.execute("DROP TRIGGER check_date_before_insert ON events ")
    op.execute("DROP FUNCTION check_date_on_insert ")
