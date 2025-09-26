"""create_users_table

Revision ID: 001_create_users_table
Revises:
Create Date: 2024-01-25 10:00:00.000000

"""

from alembic import op
from sqlalchemy import Column, Integer, String, text
from sqlalchemy.schema import FetchedValue

# revision identifiers, used by Alembic.
revision = "001_create_users_table"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        Column(
            "id",
            Integer,
            primary_key=True,
            server_default=text("nextval('users_id_seq')"),
            autoincrement=True,
        ),
        Column("email", String(255), nullable=False, unique=True),
        Column("password_hash", String(128), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("users")
    op.execute("DROP SEQUENCE IF EXISTS users_id_seq")