from sqlmodel import select, func, col
from app.models import Message, MessageCreate, Group
from app.schema.base_model import KeyValueModel
from app.services.api import PaginationService
from app.schema.api import PaginatedMessage
from app.schema.models import MessageDataList
from app.utils.exceptions import NotFoundException
from .base import BaseModelService
from app.utils.media_type import get_media_type


class MessageService(BaseModelService):
    async def _validate_group(self, data: MessageCreate) -> None:
        try:
            await self._get(model=Group, model_id=data.group_id)
        except NotFoundException:
            raise NotFoundException(msg="Группа не найдена")

    async def _validate_messages(self, data: MessageCreate) -> None:
        message_ids = list(set(list(data.parents.values()) + list(data.childrens.values())))
        result = await self.session.exec(
            select(func.count()).where(col(Message.id).in_(message_ids))
        )
        if result.one() != len(message_ids):
            raise NotFoundException(msg="Не все сообщения родителей и детей найдены")

    async def _get_media_types(self, data: MessageCreate) -> list[str]:
        media_types = []
        for media_url in data.media:
            media_type = await get_media_type(media_url=media_url)
            media_types.append(media_type.value)
        return media_types

    async def create(self, data: MessageCreate) -> Message:
        await self._validate_group(data=data)
        await self._validate_messages(data=data)
        media_types = await self._get_media_types(data=data)
        new_data = Message(**data.model_dump(), media_types=media_types)
        return await self._create(data=new_data, model=Message)

    async def get(self, message_id: int) -> Message:
        return await self._get(model=Message, model_id=message_id)

    async def update(self, data: MessageCreate, message_id: int) -> Message:
        await self._validate_group(data=data)
        await self._validate_messages(data=data)
        media_types = await self._get_media_types(data=data)
        new_data = Message(**data.model_dump(), media_types=media_types)
        new_data.id = message_id
        return await self._update(model=Message, model_id=message_id, data=new_data)

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
