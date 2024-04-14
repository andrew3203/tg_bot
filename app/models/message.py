import sqlalchemy as sa
from sqlmodel import Field

from app.database import metadata

from .base import BaseSQLModel


class Message(BaseSQLModel, table=True, metadata=metadata):
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
