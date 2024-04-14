"""add user_response_type model

Revision ID: a9387e3d45f9
Revises: bde2acc05d4f
Create Date: 2024-04-14 19:44:18.337921

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = "a9387e3d45f9"
down_revision = "bde2acc05d4f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user_response_type",
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("description", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("name"),
    )
    op.create_index(
        op.f("ix_user_response_type_name"), "user_response_type", ["name"], unique=True
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_user_response_type_name"), table_name="user_response_type")
    op.drop_table("user_response_type")
