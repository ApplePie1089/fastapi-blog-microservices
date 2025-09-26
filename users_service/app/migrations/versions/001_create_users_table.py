"""create_users_table

Revision ID: 001_create_users_table
Revises:
Create Date: 2024-01-25 10:00:00.000000

"""

from alembic import op
from sqlalchemy import Column, Integer, String, text, Enum
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.schema import FetchedValue
from sqlalchemy.sql import func

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
        Column("role", Enum('USER_ROLE_UNSPECIFIED', 'USER_ROLE_USER', 'USER_ROLE_ADMIN', name='userrole'), nullable=False, server_default='USER_ROLE_USER'),
        Column(
            "created_at",
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=func.now(),
        ),
        Column(
            "updated_at",
            TIMESTAMP(timezone=True),
            nullable=True,
            server_default=func.now(),
            server_onupdate=FetchedValue(),
        ),
    )

    op.execute(
        """
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ language 'plpgsql';
        """
    )

    op.execute(
        """
        CREATE TRIGGER update_users_updated_at BEFORE UPDATE
        ON users FOR EACH ROW EXECUTE PROCEDURE
        update_updated_at_column();
        """
    )


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS update_users_updated_at ON users")
    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column()")
    op.drop_table("users")
    op.execute("DROP SEQUENCE IF EXISTS users_id_seq")
    op.execute("DROP TYPE IF EXISTS userrole")