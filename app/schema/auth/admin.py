from ..base_model import BaseModel
from pydantic import Field, EmailStr


class AdminLoginModel(BaseModel):
    """
    Admin login data
        - `email`
        - `password`
    """

    email: EmailStr = Field(description="Email")
    password: str = Field(description="Password")


class AdminSignupModel(AdminLoginModel):
    """
    Admin signup data
        - `name`
        - `email`
        - `password`
    """

    name: str = Field(description="Name")
