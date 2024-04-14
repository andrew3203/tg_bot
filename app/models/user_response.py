from sqlmodel import Field

from app.database import metadata

from .base import BaseSQLModel


class UserResponseType(BaseSQLModel, table=True, metadata=metadata):
    """
    UserResponseType:
        - `id`
        - `name`
        - `created_at`
        - `updated_at`
    """

    __tablename__ = "user_response_type"
    __verbouse_name__ = "Тип ответа пользователя"

    name: str = Field(description="Name", unique=True)


class UserResponse(BaseSQLModel, table=True, metadata=metadata):
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

    user_id: int = Field(primary_key=True, foreign_key="user.id")
    message_id: int = Field(primary_key=True, foreign_key="message.id")
    response_type_id: int = Field(
        description="Response type", foreign_key="user_response_type.id"
    )

    text: str | None = Field(description="Response text", default=None, nullable=True)
