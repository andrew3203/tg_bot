from pydantic import Field

from .base_model import BaseModel


class ExeptionData(BaseModel):
    code: int = Field(description="Код ошибки")
    msg: str = Field(description="Сообщение ошибки")
    detail: str | None = Field(default=None, description="Доп. информация об ошибке")
