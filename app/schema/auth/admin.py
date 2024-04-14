from ..base_model import BaseModel
from pydantic import Field


class AdminLoginModel(BaseModel):
    """
    Admin login data
        - `email`
        - `password`
    """

    email: str = Field(description="Email")
    password: str = Field(description="Password")
