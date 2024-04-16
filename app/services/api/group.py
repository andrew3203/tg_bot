from sqlmodel import select
from app.models import Group, GroupCreate, User, Message
from app.schema.base_model import KeyValueModel
from app.services.api.pagination import PaginationService
from app.schema.api import PaginatedGroup
from app.utils.exceptions import DataExeption
from .base import BaseModelService


class GroupService(BaseModelService):
    async def create(self, data: GroupCreate) -> Group:
        return await self._create(data=data, model=Group)

    async def get(self, group_id: int) -> Group:
        return await self._get(model=Group, model_id=group_id)

    async def update(self, data: GroupCreate, group_id: int) -> Group:
        return await self._update(model=Group, model_id=group_id, data=data)

    async def _chech_user_exsists(self, group: Group) -> None:
        result = await self.session.exec(select(User).where(User.group_id == group.id))
        if result.one_or_none() is not None:
            raise DataExeption(
                msg="Вы не можете удалить этот обьект, есть связанные обьекты"
            )

    async def _chech_message_exsists(self, group: Group) -> None:
        result = await self.session.exec(
            select(Message).where(Message.group_id == group.id)
        )
        if result.one_or_none() is not None:
            raise DataExeption(
                msg="Вы не можете удалить этот обьект, есть связанные обьекты"
            )

    async def delete(self, group_id: int) -> KeyValueModel:
        group = await self._get(model=Group, model_id=group_id)
        await self._chech_user_exsists(group=group)
        await self._chech_message_exsists(group=group)

        await self.session.delete(group)
        await self.session.commit()
        return KeyValueModel(key="OK", value="Обьект удален")

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
