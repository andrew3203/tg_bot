"""add broadcast model

Revision ID: f9c336736e44
Revises: d2c06cdbd6dd
Create Date: 2024-04-14 19:49:18.142325

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = "f9c336736e44"
down_revision = "d2c06cdbd6dd"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "broadcast",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("group_id", sa.Integer(), nullable=False),
        sa.Column("message_id", sa.Integer(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("planned_quantity", sa.Integer(), nullable=False),
        sa.Column("succeded_quantity", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column("start_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("end_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["group_id"],
            ["group.id"],
        ),
        sa.ForeignKeyConstraint(
            ["message_id"],
            ["message.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_broadcast_group_id"), "broadcast", ["group_id"], unique=False
    )
    op.create_index(op.f("ix_broadcast_id"), "broadcast", ["id"], unique=True)
    op.create_index(
        op.f("ix_broadcast_message_id"), "broadcast", ["message_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_broadcast_message_id"), table_name="broadcast")
    op.drop_index(op.f("ix_broadcast_id"), table_name="broadcast")
    op.drop_index(op.f("ix_broadcast_group_id"), table_name="broadcast")
    op.drop_table("broadcast")
