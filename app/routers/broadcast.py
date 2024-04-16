from typing import Annotated
from fastapi import APIRouter, Depends, Query, Request
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_async_session
from app.schema.api import PaginatedBroadcast
from app.services.api import PaginationService, BroadcastService
from app.services.auth import get_current_user
from app.schema.auth import TokeModel
from app.models import Broadcast, BroadcastCreate


router = APIRouter(prefix="/broadcast", tags=["broadcast"])


@router.get(
    "",
    response_model=Broadcast,
)
async def get_broadcast(
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
    broadcast_id: int = Query(description="Broadcast ID", gt=0),
) -> Broadcast:
    service = BroadcastService(token_model=token_model, session=session)
    return await service.get(broadcast_id=broadcast_id)


@router.post(
    "",
    response_model=Broadcast,
)
async def create_broadcast(
    data: BroadcastCreate,
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
) -> Broadcast:
    service = BroadcastService(token_model=token_model, session=session)
    return await service.create(data=data)


@router.put(
    "",
    response_model=Broadcast,
)
async def update_broadcast(
    data: BroadcastCreate,
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
    broadcast_id: int = Query(description="Broadcast ID", gt=0),
) -> Broadcast:
    service = BroadcastService(token_model=token_model, session=session)
    return await service.update(data=data, broadcast_id=broadcast_id)


@router.put(
    "/cancel",
    response_model=Broadcast,
)
async def cancel_broadcast(
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
    broadcast_id: int = Query(description="Broadcast ID", gt=0),
) -> Broadcast:
    service = BroadcastService(token_model=token_model, session=session)
    return await service.cancel_broadcast(broadcast_id=broadcast_id)


@router.get(
    "/list",
    response_model=PaginatedBroadcast,
)
async def get_broadcast_list(
    request: Request,
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
    page_number: int = Query(description="Номер страницы в выдаче", default=1, ge=1),
    page_limit: int = Query(
        description="Кол-во обьектов на странице", default=10, ge=5
    ),
) -> PaginatedBroadcast:
    service = BroadcastService(token_model=token_model, session=session)
    pagination = PaginationService(request_url=request.url)
    return await service.list(
        page_number=page_number, page_limit=page_limit, service=pagination
    )
