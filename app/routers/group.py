from typing import Annotated
from fastapi import APIRouter, Depends, Query, Request
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_async_session
from app.schema.api import PaginatedGroup
from app.services.api import PaginationService, GroupService
from app.services.api.auth import get_current_user
from app.schema.auth import TokeModel
from app.models import Group, GroupCreate


router = APIRouter(prefix="/group", tags=["group"])


@router.get(
    "",
    response_model=Group,
)
async def get_group(
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
    group_id: int = Query(description="Group ID", gt=0),
) -> Group:
    service = GroupService(token_model=token_model, session=session)
    return await service.get(group_id=group_id)


@router.post(
    "",
    response_model=Group,
)
async def create_group(
    data: GroupCreate,
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
) -> Group:
    service = GroupService(token_model=token_model, session=session)
    return await service.create(data=data)


@router.put(
    "",
    response_model=Group,
)
async def update_group(
    data: GroupCreate,
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
    group_id: int = Query(description="Group ID", gt=0),
) -> Group:
    service = GroupService(token_model=token_model, session=session)
    return await service.update(data=data, group_id=group_id)


@router.get(
    "/list",
    response_model=PaginatedGroup,
)
async def get_group_list(
    request: Request,
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
    page_number: int = Query(description="Номер страницы в выдаче", default=1, ge=1),
    page_limit: int = Query(
        description="Кол-во обьектов на странице", default=10, ge=5
    ),
) -> PaginatedGroup:
    service = GroupService(token_model=token_model, session=session)
    pagination = PaginationService(request_url=request.url)
    return await service.list(
        page_number=page_number, page_limit=page_limit, service=pagination
    )
