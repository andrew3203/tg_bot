from sqlmodel import select
from app.models import User, UserCreate, Group
from app.services.api import PaginationService
from app.schema.api import PaginatedUser
from app.utils.exceptions import NotFoundException
from .base import BaseModelService


class UserService(BaseModelService):
    async def _validate_group(self, data: UserCreate) -> None:
        try:
            await self._get(model=Group, model_id=data.group_id)
        except NotFoundException:
            raise NotFoundException(msg="Группа не найдена")

    async def create(self, data: UserCreate) -> User:
        await self._validate_group(data=data)
        return await self._create(data=data, model=User)

    async def get(self, user_id: int) -> User:
        return await self._get(model=User, model_id=user_id)

    async def update(self, data: UserCreate, user_id: int) -> User:
        await self._validate_group(data=data)
        return await self._update(model=User, model_id=user_id, data=data)

    async def list(
        self, service: PaginationService, page_number: int = 1, page_limit: int = 10
    ) -> PaginatedUser:
        return await self._list(
            schema=PaginatedUser,
            service=service,
            statement=select(User),
            page_number=page_number,
            page_limit=page_limit,
        )
