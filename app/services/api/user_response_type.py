from sqlmodel import select, func
from app.models import UserResponseType, UserResponseTypeCreate, UserResponse
from app.schema.base_model import KeyValueModel
from app.services.api.pagination import PaginationService
from app.schema.api import PaginatedUserResponseType
from app.utils.exceptions import DataExeption, NotFoundException
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

    async def get(self, user_response_type_name: str) -> UserResponseType:
        result = await self.session.exec(
            select(UserResponseType).where(
                UserResponseType.name == user_response_type_name
            )
        )
        user_resonse_type = result.one_or_none()
        if user_resonse_type is None:
            raise NotFoundException(msg="Обьект не найден")
        return user_resonse_type

    async def update(
        self, data: UserResponseTypeCreate, user_response_type_id: int
    ) -> UserResponseType:
        await self._validate_name(data=data)
        return await self._update(
            model=UserResponseType, model_id=user_response_type_id, data=data
        )

    async def _chech_user_response_exsists(
        self, user_resonse_type: UserResponseType
    ) -> None:
        result = await self.session.exec(
            select(UserResponse).where(
                UserResponse.response_type_name == user_resonse_type.name
            )
        )
        if result.one_or_none() is not None:
            raise DataExeption(
                msg="Вы не можете удалить этот обьект, есть связанные обьекты"
            )

    async def delete(self, user_response_type_name: str) -> KeyValueModel:
        user_resonse_type = await self.get(
            user_response_type_name=user_response_type_name
        )
        await self._chech_user_response_exsists(user_resonse_type=user_resonse_type)
        await self.session.delete(user_resonse_type)
        await self.session.commit()
        return KeyValueModel(key="OK", value="Обьект удален")

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
