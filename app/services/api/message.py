from sqlmodel import select, func, col
from app.models import Message, MessageCreate, Group
from app.schema.base_model import KeyValueModel
from app.services.api import PaginationService
from app.schema.api import PaginatedMessage
from app.utils.exceptions import NotFoundException
from .base import BaseModelService


class MessageService(BaseModelService):
    async def _validate_group(self, data: MessageCreate) -> None:
        try:
            await self._get(model=Group, model_id=data.group_id)
        except NotFoundException:
            raise NotFoundException(msg="Группа не найдена")

    async def _validate_messages(self, data: MessageCreate) -> None:
        message_ids = data.parents + data.childrens
        result = await self.session.exec(
            select(func.count()).where(col(Message.id).in_(message_ids))
        )
        if result.one() != len(message_ids):
            raise NotFoundException(msg="Не все сообщения родителей и детей найдены")

    async def create(self, data: MessageCreate) -> Message:
        await self._validate_group(data=data)
        await self._validate_messages(data=data)
        return await self._create(data=data, model=Message)

    async def get(self, message_id: int) -> Message:
        return await self._get(model=Message, model_id=message_id)

    async def update(self, data: MessageCreate, message_id: int) -> Message:
        await self._validate_group(data=data)
        await self._validate_messages(data=data)
        return await self._update(model=Message, model_id=message_id, data=data)

    async def delete(self, message_id: int) -> KeyValueModel:
        return await self._delete(model=Message, model_id=message_id)

    async def list(
        self, service: PaginationService, page_number: int = 1, page_limit: int = 10
    ) -> PaginatedMessage:
        return await self._list(
            schema=PaginatedMessage,
            service=service,
            statement=select(Message),
            page_number=page_number,
            page_limit=page_limit,
        )
