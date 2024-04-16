from datetime import UTC, datetime
from typing import Literal
from sqlmodel import select, func
from app.models import Broadcast, BroadcastCreate, Group, Message, User
from app.schema.base_model import KeyValueModel
from app.services.api.pagination import PaginationService
from app.schema.api import PaginatedBroadcast
from app.utils.exceptions import NotFoundException, DataExeption
from .base import BaseModelService


class BroadcastService(BaseModelService):
    async def _validate_group(self, data: BroadcastCreate) -> Group:
        try:
            return await self._get(model=Group, model_id=data.group_id)
        except NotFoundException:
            raise NotFoundException(msg="Группа не найдена")

    async def _validate_message(self, data: BroadcastCreate) -> Message:
        try:
            return await self._get(model=Message, model_id=data.message_id)
        except NotFoundException:
            raise NotFoundException(msg="Сообщение не найдено")

    async def _count_group_users(self, group: Group) -> int:
        result = await self.session.exec(
            select(func.count()).where(User.group_id == group.id)
        )
        return result.one()

    async def create(self, data: BroadcastCreate) -> Broadcast:
        group = await self._validate_group(data=data)
        await self._validate_message(data=data)

        status: Literal[
            "planned", "running", "succeded", "failed", "cancelled"
        ] = "planned"
        if data.start_date is None:
            data.start_date = datetime.now(UTC)
            status = "running"
        elif data.start_date < datetime.now(UTC):
            raise DataExeption(msg="Нельзя создать рассылку в прошлом")

        planned_quantity = await self._count_group_users(group=group)
        _broadcast = Broadcast(**data.model_dump(), planned_quantity=planned_quantity)
        _broadcast.status = status
        self.session.add(_broadcast)
        await self.session.commit()
        # TODO: run broadcast
        return _broadcast

    async def get(self, broadcast_id: int) -> Broadcast:
        return await self._get(model=Broadcast, model_id=broadcast_id)

    async def update(self, data: BroadcastCreate, broadcast_id: int) -> Broadcast:
        status: Literal[
            "planned", "running", "succeded", "failed", "cancelled"
        ] = "planned"
        if data.start_date is None:
            data.start_date = datetime.now(UTC)
            status = "running"
        elif data.start_date < datetime.now(UTC):
            raise DataExeption(msg="Нельзя изменить рассылку в прошлом")

        _broadcast = await self._get(model=Broadcast, model_id=broadcast_id)
        if _broadcast.status not in ("failed", "cancelled", "succeded"):
            raise DataExeption(
                msg="Рассылка не может быть изменена (только при failed, cancelled, succeded)"
            )

        group = await self._validate_group(data=data)
        await self._validate_message(data=data)
        _broadcast.status = status
        _broadcast.planned_quantity = await self._count_group_users(group=group)
        _broadcast.succeded_quantity = 0
        _broadcast.end_date = None

        await self._set_params(model=_broadcast, data=data)
        self.session.add(_broadcast)
        await self.session.commit()
        # TODO: run broadcast
        return _broadcast

    async def delete(self, broadcast_id: int) -> KeyValueModel:
        _broadcast = await self._get(model=Broadcast, model_id=broadcast_id)
        if _broadcast.status not in ("failed", "cancelled", "succeded"):
            raise DataExeption(
                msg="Рассылка не может быть удалена (только при failed, cancelled, succeded)"
            )
        await self.session.delete(_broadcast)
        await self.session.commit()
        return KeyValueModel(key="OK", value="Обьект удален")

    async def cancel_broadcast(self, broadcast_id: int) -> Broadcast:
        _broadcast = await self._get(model=Broadcast, model_id=broadcast_id)
        _broadcast.status = "cancelled"
        self.session.add(_broadcast)
        await self.session.commit()
        # TODO: run cancel broadcast
        return _broadcast

    async def list(
        self, service: PaginationService, page_number: int = 1, page_limit: int = 10
    ) -> PaginatedBroadcast:
        return await self._list(
            schema=PaginatedBroadcast,
            service=service,
            statement=select(Broadcast),
            page_number=page_number,
            page_limit=page_limit,
        )
