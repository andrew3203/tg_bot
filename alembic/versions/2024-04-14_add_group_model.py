"""add group model

Revision ID: cfbe890efc1c
Revises: 
Create Date: 2024-04-14 19:42:43.289535

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = "cfbe890efc1c"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "group",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "criterion_field", sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
        sa.Column(
            "criterion_field_type", sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
        sa.Column(
            "criterion_value", sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
        sa.Column("criterion_value_type", sa.String(), nullable=True),
        sa.Column("criterion_rule", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_group_id"), "group", ["id"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_group_id"), table_name="group")
    op.drop_table("group")
