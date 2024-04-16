from datetime import UTC, datetime
from sqlmodel import Field, SQLModel
import sqlalchemy as sa
from app.database import metadata


class AdminCreate(SQLModel, table=False, metadata=None):
    """
    User:
        - name
        - is_superuser
        - is_active
        - email
        - hashed_password
    """

    name: str = Field(description="Admin name")
    is_superuser: bool = Field(description="Is superuser", default=False)
    is_active: bool = Field(description="Is active", default=True)
    email: str = Field(description="Email")
    hashed_password: bytes = Field(description="Hashed password")


class Admin(AdminCreate, table=True, metadata=metadata):
    """
    User:
        - id
        - name
        - is_superuser
        - is_active
        - email
        - hashed_password
        - created_at
        - updated_at
    """

    __tablename__ = "admin"
    __verbouse_name__ = "Админ"

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
