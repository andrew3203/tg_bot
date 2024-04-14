from datetime import UTC, datetime

import sqlalchemy as sa
from sqlmodel import Field, SQLModel


class BaseSQLModel(SQLModel, table=False):
    """
    Base model with common fields:
        - `id`
        - `created_at`
        - `updated_at`
    """

    id: int = Field(
        primary_key=True,
        index=True,
        description="Primary key",
    )
    created_at: datetime = Field(
        default=datetime.now(UTC),
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False),
        description="Created at",
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_column=sa.Column(sa.DateTime(timezone=True)),
        description="Updated at",
    )
