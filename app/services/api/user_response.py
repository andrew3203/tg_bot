from sqlmodel import select, func
from app.models import UserResponse, UserResponseCreate, Message, User, UserResponseType
from app.services.api.pagination import PaginationService
from app.schema.api import PaginatedUserResponse
from app.utils.exceptions import DataExeption, NotFoundException
from .base import BaseModelService


class UserResponseService(BaseModelService):
    async def _validate_message(self, data: UserResponseCreate) -> Message:
        try:
            return await self._get(model=Message, model_id=data.message_id)
        except NotFoundException:
            raise NotFoundException(msg="Сообщение не найдено")

    async def _validate_user(self, data: UserResponseCreate) -> User:
        try:
            return await self._get(model=User, model_id=data.user_id)
        except NotFoundException:
            raise NotFoundException(msg="Пользователь не найден")

    async def _validate_name(self, data: UserResponseCreate) -> None:
        result = await self.session.exec(
            select(func.count()).where(UserResponseType.name == data.response_type_name)
        )
        if result.one() != 0:
            raise DataExeption(msg="Тип отклика не существует")

    async def create(self, data: UserResponseCreate) -> UserResponse:
        await self._validate_message(data=data)
        await self._validate_user(data=data)
        await self._validate_name(data=data)
        return await self._create(data=data, model=UserResponse)

    async def get(self, user_response_id: int) -> UserResponse:
        return await self._get(model=UserResponse, model_id=user_response_id)

    async def update(
        self, data: UserResponseCreate, user_response_id: int
    ) -> UserResponse:
        await self._validate_message(data=data)
        await self._validate_user(data=data)
        await self._validate_name(data=data)
        return await self._update(
            model=UserResponse, model_id=user_response_id, data=data
        )

    async def list(
        self, service: PaginationService, page_number: int = 1, page_limit: int = 10
    ) -> PaginatedUserResponse:
        return await self._list(
            schema=PaginatedUserResponse,
            service=service,
            statement=select(UserResponse),
            page_number=page_number,
            page_limit=page_limit,
        )
