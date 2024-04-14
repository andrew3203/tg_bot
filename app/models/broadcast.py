from datetime import datetime
from typing import Literal

import sqlalchemy as sa
from sqlmodel import Field

from app.database import metadata

from .base import BaseSQLModel


class Broadcast(BaseSQLModel, table=True, metadata=metadata):
    """
    Broadcast:
        - `id`
        - `name`
        - `group_id`
        - `message_id`
        - `planned_quantity`
        - `succeded_quantity`
        - `status`
        - `start_date`
        - `end_date`
        - `created_at`
        - `updated_at`
    """

    __tablename__ = "broadcast"
    __verbouse_name__ = "Рассылка"

    group_id: int = Field(primary_key=True, index=True, foreign_key="group.id")
    message_id: int = Field(primary_key=True, index=True, foreign_key="message.id")

    name: str = Field(description="Broadcast name")

    planned_quantity: int = Field(description="Planned quantity")
    succeded_quantity: int = Field(description="Succeded quantity")

    status: Literal["planned", "running", "succeded", "failed"] = Field(
        sa_column=sa.Column(sa.String),
        description="Status",
    )
    start_date: datetime | None = Field(
        sa_column=sa.Column(sa.DateTime(timezone=True)),
        default=None,
        description="Start date",
    )
    end_date: datetime | None = Field(
        sa_column=sa.Column(sa.DateTime(timezone=True)),
        default=None,
        description="End date",
    )
