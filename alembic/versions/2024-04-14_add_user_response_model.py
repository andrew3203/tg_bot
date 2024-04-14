"""add user_response model

Revision ID: d2c06cdbd6dd
Revises: 6ee2cf7b1737
Create Date: 2024-04-14 19:46:16.321842

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = "d2c06cdbd6dd"
down_revision = "6ee2cf7b1737"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user_response",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("message_id", sa.Integer(), nullable=False),
        sa.Column(
            "response_type_name", sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
        sa.Column("text", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["message_id"],
            ["message.id"],
        ),
        sa.ForeignKeyConstraint(
            ["response_type_name"],
            ["user_response_type.name"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_response_id"), "user_response", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_user_response_id"), table_name="user_response")
    op.drop_table("user_response")
