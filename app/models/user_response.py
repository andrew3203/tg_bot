from sqlmodel import Field, SQLModel
from datetime import UTC, datetime
from app.database import metadata
import sqlalchemy as sa


class UserResponseType(SQLModel, table=True, metadata=metadata):
    """
    UserResponseType:
        - `name`
        - `description`
        - `created_at`
        - `updated_at`
    """

    __tablename__ = "user_response_type"
    __verbouse_name__ = "Тип ответа пользователя"

    name: str = Field(description="Name", primary_key=True, index=True, unique=True)
    description: str = Field(description="Description", nullable=True)

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


class UserResponse(SQLModel, table=True, metadata=metadata):
    """
    UserResponse:
        - `id`
        - `user_id`
        - `message_id`
        - `response_type_id`
        - `text`
        - `created_at`
        - `updated_at`
    """

    __tablename__ = "user_response"
    __verbouse_name__ = "Ответ пользователя"

    id: int = Field(primary_key=True, index=True, description="Primary key")
    user_id: int = Field(foreign_key="user.id", description="User id")
    message_id: int = Field(foreign_key="message.id", description="Message id")
    response_type_name: str = Field(
        foreign_key="user_response_type.name", description="Response type name"
    )

    text: str | None = Field(description="Response text", default=None, nullable=True)

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
