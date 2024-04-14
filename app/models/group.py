from typing import Literal

import sqlalchemy as sa
from sqlmodel import Field

from app.database import metadata

from .base import BaseSQLModel


class Group(BaseSQLModel, table=True, metadata=metadata):
    """
    Group:
        - `id`
        - `name`
        - `criterion_field`
        - `criterion_field_type`
        - `criterion_value`
        - `criterion_value_type`
        - `criterion_rule`
        - `created_at`
        - `updated_at`
    """

    __tablename__ = "group"
    __verbouse_name__ = "Группа"

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
