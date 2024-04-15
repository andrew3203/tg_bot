from datetime import UTC, datetime
from typing import Any

import sqlalchemy as sa
from sqlmodel import Field, SQLModel

from app.database import metadata
from app.schema.models import ActionType


class ActionCreate(SQLModel, table=False, metadata=None):
    """
    Action:
        - message_id
        - action_type
        - params
        - name
        - run_amount
        - succeded_amount
    """

    message_id: int = Field(primary_key=True, index=True, foreign_key="message.id")

    action_type: ActionType = Field(
        sa_column=sa.Column(sa.String), description="Action type"
    )
    params: dict[str, Any] = Field(
        description="Action params", sa_column=sa.Column(sa.JSON)
    )

    name: str = Field(description="Action name")
    run_amount: int = Field(default=0, description="Run amount")
    succeded_amount: int = Field(default=0, description="Succeded amount")


class Action(ActionCreate, table=True, metadata=metadata):
    """
    Action:
        - id
        - message_id
        - action_type
        - params
        - name
        - run_amount
        - succeded_amount
        - created_at
        - updated_at
    """

    __tablename__ = "action"
    __verbouse_name__ = "Действие"

    id: int = Field(
        primary_key=True, index=True, unique=True, description="Primary key"
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
