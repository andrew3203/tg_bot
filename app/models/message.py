import sqlalchemy as sa
from sqlmodel import Field, SQLModel
from datetime import UTC, datetime
from app.database import metadata


class Message(SQLModel, table=True, metadata=metadata):
    """
    Message:
        - `id`
        - `group_id`
        - `parents`
        - `childrens`
        - `name`
        - `text`
        - `media`
        - `click_amount`
        - `uclick_amount`
        - `created_at`
        - `updated_at`
    """

    __tablename__ = "message"
    __verbouse_name__ = "Сообщение"

    id: int = Field(
        primary_key=True, index=True, unique=True, description="Primary key"
    )
    group_id: int = Field(primary_key=True, foreign_key="group.id")
    parents: list[int] = Field(
        sa_column=sa.Column(sa.ARRAY(sa.Integer), default=[]),
        description="Message parents",
    )
    childrens: list[int] = Field(
        sa_column=sa.Column(sa.ARRAY(sa.Integer), default=[]),
        description="Message childrens",
    )

    name: str = Field(description="Message name")
    text: str = Field(description="Message text")
    media: list[str] = Field(
        sa_column=sa.Column(sa.ARRAY(sa.String), default=[]),
        description="Message media",
    )

    click_amount: int = Field(default=0, description="Click amount")
    uclick_amount: int = Field(default=0, description="Unique click amount")

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