"""empty message

Revision ID: c35324722457
Revises: 34c66d2f1f8e
Create Date: 2024-06-16 11:53:38.574052

"""

from typing import Sequence, Union
from app.constants.admin import Admin
from app.utils.hash_service import HashService
import os
from dotenv import load_dotenv
from alembic import op
import sqlalchemy as sa

load_dotenv()

# revision identifiers, used by Alembic.
revision: str = "c35324722457"
down_revision: Union[str, None] = "34c66d2f1f8e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


email = Admin.EMAIL.value
phone = Admin.PHONE.value
hashed_password = HashService.hash_password(os.getenv("ADMIN_PASSWORD")).decode()


def upgrade() -> None:
    op.execute(
        f"INSERT INTO users(username,email,phone,password,role_id) VALUES ('admin','{email}','{phone}','{hashed_password}','ADMIN')"
    )


def downgrade() -> None:
    op.execute("DELETE FROM users WHERE username = 'admin' ")
