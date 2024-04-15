from typing import Any
from collections.abc import Sequence
from pydantic import Field, HttpUrl

from ..base_model import BaseModel


class PaginatedDataBase(BaseModel):
    """
    #### Модель обертка для пагинации

    `Fields`:

        :`page_number` - Номер текущей страницы
        :`page_limit` - Кол-во обьектов на странице
        :`count` - Общее кол-во обьектов
        :`prev` - Ссылка на предидущую страницу
        :`next` -  Ссылка на следующую страницу
    """

    page_number: int = Field(description="Номер текущей страницы", ge=1)
    page_limit: int = Field(description="Кол-во обьектов на странице", ge=1)
    count: int = Field(description="Общее кол-во обьектов", ge=0)
    prev: HttpUrl | None = Field(
        description="Ссылка на предидущую страницу", default=None
    )
    next: HttpUrl | None = Field(
        description="Ссылка на следующую страницу", default=None
    )
    data: Sequence[Any] = Field(description="Данные", default=[])
