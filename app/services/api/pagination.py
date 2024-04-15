from collections.abc import Sequence
from typing import NamedTuple, TypeVar

from fastapi.datastructures import URL
from pydantic import HttpUrl

from app.schema.api import PaginatedDataBase
from app.utils.exceptions import NotFoundException
from sqlmodel import SQLModel


class LimitOffset(NamedTuple):
    limit: int
    offset: int
    pages_number: int


class PrevNextLinks(NamedTuple):
    prev: HttpUrl | None
    next: HttpUrl | None


PaginatedData = TypeVar("PaginatedData", bound=PaginatedDataBase)


class PaginationService:
    def __init__(
        self,
        request_url: URL,
    ) -> None:
        self.request_url = request_url

    async def _get_limit_offset(
        self,
        page_number: int,
        page_limit: int,
        count: int,
    ) -> LimitOffset:
        """
        Метод позволяет получить `limit` и `offset` для пагинации

        `params`:
            :`page` - номер запрашиваемой страницы,
            :`page_limit` - кол-во обектов на странице
            :`count` - общее кол-во обьектов в выдаче
        """
        pages_number = count // page_limit
        if count % page_limit > 0:
            pages_number += 1

        if page_number > pages_number:
            raise NotFoundException(
                msg=f"Вы запрашиваете не существующую страницу {page_number} > {pages_number}"
            )

        return LimitOffset(
            limit=page_limit,
            offset=(page_number - 1) * page_limit,
            pages_number=pages_number,
        )

    async def _get_prev_next_links(
        self,
        page_number: int,
        pages_number: int,
        page_limit: int,
    ) -> PrevNextLinks:
        prev = None

        if page_number > 1:
            prev = HttpUrl(
                str(
                    self.request_url.include_query_params(
                        page_number=page_number - 1, page_limit=page_limit
                    )
                )
            )

        next = None
        if pages_number - 1 >= page_number:
            next = HttpUrl(
                str(
                    self.request_url.include_query_params(
                        page_number=page_number + 1, page_limit=page_limit
                    )
                )
            )

        return PrevNextLinks(prev=prev, next=next)

    async def list(
        self,
        data: Sequence[SQLModel],
        schema: type[PaginatedData],
        count: int,
        page_number: int,
        page_limit: int,
    ):
        limit_offset = await self._get_limit_offset(
            page_number=page_number, page_limit=page_limit, count=count
        )
        links = await self._get_prev_next_links(
            page_number=page_number,
            pages_number=limit_offset.pages_number,
            page_limit=page_limit,
        )

        return schema(
            page_number=page_number,
            page_limit=page_limit,
            count=count,
            prev=links.prev,
            next=links.next,
            data=data,
        )
