from typing import Literal
from datetime import UTC, datetime
import sqlalchemy as sa
from sqlmodel import Field, SQLModel

from app.database import metadata


class GroupCreate(SQLModel, table=False):
    """
    Group Create:

        - id
        - name
        - criterion_field
        - criterion_field_type
        - criterion_value
        - criterion_value_type
        - criterion_rule
        - created_at
        - updated_at
    """

    name: str = Field(description="Group name")
    criterion_field: str = Field(description="Criterion field")
    criterion_field_type: str = Field(description="Criterion field type")
    criterion_value: str = Field(description="Criterion value")
    criterion_value_type: Literal["str", "int", "float", "bool"] = Field(
        sa_column=sa.Column(sa.String),
        description="Criterion value type",
    )
    criterion_rule: Literal["=", "<", "<=", ">", ">=", "!="] = Field(
        sa_column=sa.Column(sa.String),
        description="Criterion rule",
    )


class Group(GroupCreate, table=True, metadata=metadata):
    """
    Group:

        - id
        - name
        - criterion_field
        - criterion_field_type
        - criterion_value
        - criterion_value_type
        - criterion_rule
        - created_at
        - updated_at
    """

    __tablename__ = "group"
    __verbouse_name__ = "Группа"

    id: int | None = Field(
        primary_key=True,
        index=True,
        unique=True,
        default=None,
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
