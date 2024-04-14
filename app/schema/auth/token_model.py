from typing import Literal
from pydantic import Field, AliasChoices

from ..base_model import BaseModel


class TokeModel(BaseModel):
    id: int = Field(
        description="User ID",
        validation_alias=AliasChoices("u, id"),
    )
    role: Literal["admin", "user"] = Field(
        description="User role",
        validation_alias=AliasChoices("r, role"),
    )

    @property
    def is_admin(self):
        return self.role == "admin"
