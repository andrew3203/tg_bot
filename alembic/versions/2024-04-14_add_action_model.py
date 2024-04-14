"""add action model

Revision ID: d379ea6810fb
Revises: f68af93bc03a
Create Date: 2024-04-14 19:51:42.673989

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = "d379ea6810fb"
down_revision = "f68af93bc03a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "action",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("message_id", sa.Integer(), nullable=False),
        sa.Column("action_type", sa.String(), nullable=True),
        sa.Column("params", sa.JSON(), nullable=True),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("run_amount", sa.Integer(), nullable=False),
        sa.Column("succeded_amount", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["message_id"],
            ["message.id"],
        ),
        sa.PrimaryKeyConstraint("id", "message_id"),
    )
    op.create_index(op.f("ix_action_id"), "action", ["id"], unique=True)
    op.create_index(
        op.f("ix_action_message_id"), "action", ["message_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_action_message_id"), table_name="action")
    op.drop_index(op.f("ix_action_id"), table_name="action")
    op.drop_table("action")
