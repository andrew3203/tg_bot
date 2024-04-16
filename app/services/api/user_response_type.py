from sqlmodel import select, func
from app.models import UserResponseType, UserResponseTypeCreate
from app.services.api.pagination import PaginationService
from app.schema.api import PaginatedUserResponseType
from app.utils.exceptions import DataExeption
from .base import BaseModelService


class UserResponseTypeService(BaseModelService):
    async def _validate_name(self, data: UserResponseTypeCreate) -> None:
        result = await self.session.exec(
            select(func.count()).where(UserResponseType.name == data.name)
        )
        if result.one() > 0:
            raise DataExeption(msg="Тип отклика уже существует")

    async def create(self, data: UserResponseTypeCreate) -> UserResponseType:
        await self._validate_name(data=data)
        return await self._create(data=data, model=UserResponseType)

    async def get(self, user_response_type_id: int) -> UserResponseType:
        return await self._get(model=UserResponseType, model_id=user_response_type_id)

    async def update(
        self, data: UserResponseTypeCreate, user_response_type_id: int
    ) -> UserResponseType:
        await self._validate_name(data=data)
        return await self._update(
            model=UserResponseType, model_id=user_response_type_id, data=data
        )

    async def list(
        self, service: PaginationService, page_number: int = 1, page_limit: int = 10
    ) -> PaginatedUserResponseType:
        return await self._list(
            schema=PaginatedUserResponseType,
            service=service,
            statement=select(UserResponseType),
            page_number=page_number,
            page_limit=page_limit,
        )
