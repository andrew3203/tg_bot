"""add message model

Revision ID: bde2acc05d4f
Revises: cfbe890efc1c
Create Date: 2024-04-14 19:43:29.021754

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = "bde2acc05d4f"
down_revision = "cfbe890efc1c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "message",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("group_id", sa.Integer(), nullable=False),
        sa.Column("parents", sa.JSON(), nullable=True),
        sa.Column("childrens", sa.JSON(), nullable=True),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("tg_alias_name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("text", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("media", sa.ARRAY(sa.String()), nullable=True),
        sa.Column("media_types", sa.ARRAY(sa.String()), nullable=True),
        sa.Column("click_amount", sa.Integer(), nullable=False),
        sa.Column("uclick_amount", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["group_id"],
            ["group.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_message_id"), "message", ["id"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_message_id"), table_name="message")
    op.drop_table("message")
