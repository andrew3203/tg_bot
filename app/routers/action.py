from typing import Annotated
from fastapi import APIRouter, Depends, Query, Request
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_async_session
from app.schema.api import PaginatedAction
from app.schema.base_model import KeyValueModel
from app.services.api import PaginationService, ActionService
from app.services.api.auth import get_current_user
from app.schema.auth import TokeModel
from app.models import Action, ActionCreate


router = APIRouter(prefix="/action", tags=["action"])


@router.get(
    "",
    response_model=Action,
)
async def get_action(
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
    action_id: int = Query(description="Action ID", gt=0),
) -> Action:
    service = ActionService(token_model=token_model, session=session)
    return await service.get(action_id=action_id)


@router.post(
    "",
    response_model=Action,
)
async def create_action(
    data: ActionCreate,
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
) -> Action:
    service = ActionService(token_model=token_model, session=session)
    return await service.create(data=data)


@router.put(
    "",
    response_model=Action,
)
async def update_action(
    data: ActionCreate,
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
    action_id: int = Query(description="Action ID", gt=0),
) -> Action:
    service = ActionService(token_model=token_model, session=session)
    return await service.update(data=data, action_id=action_id)


@router.get(
    "/list",
    response_model=PaginatedAction,
)
async def get_action_list(
    request: Request,
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
    page_number: int = Query(description="Номер страницы в выдаче", default=1, ge=1),
    page_limit: int = Query(
        description="Кол-во обьектов на странице", default=10, ge=5
    ),
) -> PaginatedAction:
    service = ActionService(token_model=token_model, session=session)
    pagination = PaginationService(request_url=request.url)
    return await service.list(
        page_number=page_number, page_limit=page_limit, service=pagination
    )


@router.delete("", response_model=KeyValueModel)
async def delete_action(
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
    action_id: int = Query(description="Action ID", gt=0),
) -> KeyValueModel:
    service = ActionService(token_model=token_model, session=session)
    return await service.delete(action_id=action_id)
