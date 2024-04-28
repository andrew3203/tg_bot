from sqlmodel import select
from app.models import Action, ActionCreate, Message
from app.schema.base_model import KeyValueModel
from app.services.api.pagination import PaginationService
from app.schema.api import PaginatedAction
from app.schema.models.action import ActionDataList
from app.utils.exceptions import NotFoundException
from .base import BaseModelService


class ActionService(BaseModelService):
    async def _validate_group(self, data: ActionCreate) -> None:
        try:
            await self._get(model=Message, model_id=data.message_id)
        except NotFoundException:
            raise NotFoundException(msg="Сообщение не найдено")

    async def create(self, data: ActionCreate) -> Action:
        await self._validate_group(data=data)
        return await self._create(data=data, model=Action)

    async def get(self, action_id: int) -> Action:
        return await self._get(model=Action, model_id=action_id)

    async def update(self, data: ActionCreate, action_id: int) -> Action:
        await self._validate_group(data=data)
        return await self._update(model=Action, model_id=action_id, data=data)

    async def delete(self, action_id: int) -> KeyValueModel:
        return await self._delete(model=Action, model_id=action_id)

    async def get_list(
        self, service: PaginationService, page_number: int = 1, page_limit: int = 10
    ) -> PaginatedAction:
        statement = select(Action, Message).join(Message)
        result = await self.session.exec(statement)
        data = [
            ActionDataList(
                **action.model_dump(),
                message_name=message.name,
            )
            for action, message in result.all()
        ]
        return await service.get_list(
            data=data,
            schema=PaginatedAction,
            count=len(data),
            page_number=page_number,
            page_limit=page_limit,
        )
