from typing import Annotated
from fastapi import APIRouter, Depends, Query, Request
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_async_session
from app.schema.api import PaginatedMessage
from app.schema.base_model import KeyValueModel
from app.services.api import PaginationService, MessageService
from app.services.api.auth import get_current_user
from app.schema.auth import TokeModel
from app.models import Message, MessageCreate


router = APIRouter(prefix="/message", tags=["message"])


@router.get(
    "",
    response_model=Message,
)
async def get_message(
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
    message_id: int = Query(description="Message ID", gt=0),
) -> Message:
    service = MessageService(token_model=token_model, session=session)
    return await service.get(message_id=message_id)


@router.post(
    "",
    response_model=Message,
)
async def create_message(
    data: MessageCreate,
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
) -> Message:
    service = MessageService(token_model=token_model, session=session)
    return await service.create(data=data)


@router.put(
    "",
    response_model=Message,
)
async def update_message(
    data: MessageCreate,
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
    message_id: int = Query(description="Message ID", gt=0),
) -> Message:
    service = MessageService(token_model=token_model, session=session)
    return await service.update(data=data, message_id=message_id)


@router.get(
    "/list",
    response_model=PaginatedMessage,
)
async def get_message_list(
    request: Request,
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
    page_number: int = Query(description="Номер страницы в выдаче", default=1, ge=1),
    page_limit: int = Query(
        description="Кол-во обьектов на странице", default=10, ge=5
    ),
) -> PaginatedMessage:
    service = MessageService(token_model=token_model, session=session)
    pagination = PaginationService(request_url=request.url)
    return await service.get_list(
        page_number=page_number, page_limit=page_limit, service=pagination
    )


@router.get(
    "/names/list",
    response_model=list[KeyValueModel],
)
async def get_message_names_list(
    request: Request,
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
) -> list[KeyValueModel]:
    service = MessageService(token_model=token_model, session=session)
    return await service.names_list()


@router.delete("", response_model=KeyValueModel)
async def delete_message(
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
    message_id: int = Query(description="Message ID", gt=0),
) -> KeyValueModel:
    service = MessageService(token_model=token_model, session=session)
    return await service.delete(message_id=message_id)
