from sqlmodel import select, func, col
from app.models import Message, MessageCreate, Group
from app.schema.base_model import KeyValueModel
from app.services.api import PaginationService
from app.schema.api import PaginatedMessage
from app.schema.models import MessageDataList
from app.utils.exceptions import NotFoundException
from .base import BaseModelService


class MessageService(BaseModelService):
    async def _validate_group(self, data: MessageCreate) -> None:
        try:
            await self._get(model=Group, model_id=data.group_id)
        except NotFoundException:
            raise NotFoundException(msg="Группа не найдена")

    async def _validate_messages(self, data: MessageCreate) -> None:
        message_ids = list(data.parents.values()) + list(data.childrens.values())
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

    async def get_list(
        self, service: PaginationService, page_number: int = 1, page_limit: int = 10
    ) -> PaginatedMessage:
        statement = select(Message, Group).select_from(Message)
        result = await self.session.exec(statement)
        data = [
            MessageDataList(
                **message.model_dump(),
                group_name=group.name,
            )
            for message, group in result.all()
        ]
        return await service.get_list(
            data=data,
            schema=PaginatedMessage,
            count=len(data),
            page_number=page_number,
            page_limit=page_limit,
        )

    async def names_list(self) -> list[KeyValueModel]:
        return await self._names_list(
            model=Message,
            columns=[col(Message.id).label("key"), col(Message.name).label("value")],
        )
