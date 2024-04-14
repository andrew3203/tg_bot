"""add action model

Revision ID: f68af93bc03a
Revises: f9c336736e44
Create Date: 2024-04-14 19:50:45.560746

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = "f68af93bc03a"
down_revision = "f9c336736e44"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "admin",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("email", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("hashed_password", sa.LargeBinary(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_admin_id"), "admin", ["id"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_admin_id"), table_name="admin")
    op.drop_table("admin")
