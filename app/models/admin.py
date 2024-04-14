from sqlmodel import Field

from app.database import metadata

from .base import BaseSQLModel


class Admin(BaseSQLModel, table=True, metadata=metadata):
    """
    User:
        - `id`
        - `name`
        - `is_superuser`
        - `is_active`
        - `email`
        - `hashed_password`
        - `created_at`
        - `updated_at`
    """

    __tablename__ = "admin"
    __verbouse_name__ = "Админ"

    name: str = Field(description="Admin name")
    is_superuser: bool = Field(description="Is superuser", default=False)
    is_active: bool = Field(description="Is active", default=True)

    email: str = Field(description="Email")
    hashed_password: str = Field(description="Hashed password")
