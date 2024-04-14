from sqlmodel import Field

from app.database import metadata

from .base import BaseSQLModel


class User(BaseSQLModel, table=True, metadata=metadata):
    """
    User:
        - `id`
        - `group_id`
        - `firstname`
        - `lastname`
        - `portobello_id`
        - `company`
        - `rating`
        - `turnover`
        - `orders_amount`
        - `cashback_amount`
        - `golden_tickets_amount`
        - `created_at`
        - `updated_at`
    """

    __tablename__ = "user"
    __verbouse_name__ = "Пользователь"

    group_id: int = Field(primary_key=True, foreign_key="group.id")

    firstname: str = Field(description="Firstname")
    lastname: str | None = Field(description="Lastname", nullable=True)

    portobello_id: str = Field(description="Portobello id")

    company: str | None = Field(description="Company", nullable=True)
    rating: int | None = Field(description="Rating", nullable=True)
    turnover: int | None = Field(description="Turnover", nullable=True)
    orders_amount: int | None = Field(description="Orders amount", nullable=True)
    cashback_amount: int | None = Field(description="Cashback amount", nullable=True)
    golden_tickets_amount: int | None = Field(
        description="Golden tickets amount", nullable=True
    )
