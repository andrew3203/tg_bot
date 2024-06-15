from sqlmodel import col, select
from app.models import Group, GroupCreate, User, Message
from app.schema.base_model import KeyValueModel
from app.services.api.pagination import PaginationService
from app.schema.api import PaginatedGroup
from app.utils.exceptions import DataExeption
from .base import BaseModelService
import asyncio
from app.services.utils import apply_group_criteria


class GroupService(BaseModelService):
    async def create(self, data: GroupCreate) -> Group:
        group = await self._create(data=data, model=Group)
        await self.session.commit()
        await self._apply_group_criteria(group=group)
        return group

    async def get(self, group_id: int) -> Group:
        return await self._get(model=Group, model_id=group_id)

    async def _apply_group_criteria(self, group: Group) -> None:
        loop = asyncio.get_running_loop()
        loop.run_in_executor(None, lambda: apply_group_criteria(group=group))

    async def update(self, data: GroupCreate, group_id: int) -> Group:
        group = await self._update(model=Group, model_id=group_id, data=data)
        await self.session.commit()
        await self._apply_group_criteria(group=group)
        return group

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

    async def get_list(
        self, service: PaginationService, page_number: int = 1, page_limit: int = 10
    ) -> PaginatedGroup:
        return await self._list(
            schema=PaginatedGroup,
            service=service,
            statement=select(Group),
            page_number=page_number,
            page_limit=page_limit,
        )

    async def names_list(self) -> list[KeyValueModel]:
        return await self._names_list(
            model=Group,
            columns=[col(Group.name).label("value"), col(Group.id).label("key")],
        )
