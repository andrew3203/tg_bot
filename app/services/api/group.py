from sqlmodel import select
from app.models import Group, GroupCreate
from app.services.api.pagination import PaginationService
from app.schema.api import PaginatedGroup
from .base import BaseModelService


class GroupService(BaseModelService):
    async def create(self, data: GroupCreate) -> Group:
        return await self._create(data=data, model=Group)

    async def get(self, group_id: int) -> Group:
        return await self._get(model=Group, model_id=group_id)

    async def update(self, data: GroupCreate, group_id: int) -> Group:
        return await self._update(model=Group, model_id=group_id, data=data)

    async def list(
        self, service: PaginationService, page_number: int = 1, page_limit: int = 10
    ) -> PaginatedGroup:
        return await self._list(
            schema=PaginatedGroup,
            service=service,
            statement=select(Group),
            page_number=page_number,
            page_limit=page_limit,
        )
