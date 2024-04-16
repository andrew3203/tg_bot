from typing import Annotated
from fastapi import APIRouter, Depends, Query, Request
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_async_session
from app.schema.api import PaginatedUserResponse
from app.schema.base_model import KeyValueModel
from app.services.api import PaginationService, UserResponseService
from app.services.api.auth import get_current_user
from app.schema.auth import TokeModel
from app.models import UserResponse, UserResponseCreate


router = APIRouter(prefix="/user_response", tags=["user_response"])


@router.get(
    "",
    response_model=UserResponse,
)
async def get_user_response(
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
    user_response_id: int = Query(description="UserResponse ID", gt=0),
) -> UserResponse:
    service = UserResponseService(token_model=token_model, session=session)
    return await service.get(user_response_id=user_response_id)


@router.post(
    "",
    response_model=UserResponse,
)
async def create_user_response(
    data: UserResponseCreate,
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
) -> UserResponse:
    service = UserResponseService(token_model=token_model, session=session)
    return await service.create(data=data)


@router.put(
    "",
    response_model=UserResponse,
)
async def update_user_response(
    data: UserResponseCreate,
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
    user_response_id: int = Query(description="UserResponse ID", gt=0),
) -> UserResponse:
    service = UserResponseService(token_model=token_model, session=session)
    return await service.update(data=data, user_response_id=user_response_id)


@router.get(
    "/list",
    response_model=PaginatedUserResponse,
)
async def get_user_response_list(
    request: Request,
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
    page_number: int = Query(description="Номер страницы в выдаче", default=1, ge=1),
    page_limit: int = Query(
        description="Кол-во обьектов на странице", default=10, ge=5
    ),
) -> PaginatedUserResponse:
    service = UserResponseService(token_model=token_model, session=session)
    pagination = PaginationService(request_url=request.url)
    return await service.list(
        page_number=page_number, page_limit=page_limit, service=pagination
    )


@router.delete("", response_model=KeyValueModel)
async def delete_user_response(
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
    user_response_id: int = Query(description="UserResponse ID", gt=0),
) -> KeyValueModel:
    service = UserResponseService(token_model=token_model, session=session)
    return await service.delete(user_response_id=user_response_id)
