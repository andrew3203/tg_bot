from typing import Annotated
from fastapi import APIRouter, Depends, Query, Request
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_async_session
from app.schema.api import PaginatedUserResponseType
from app.schema.base_model import KeyValueModel
from app.services.api import PaginationService, UserResponseTypeService
from app.services.api.auth import get_current_user
from app.schema.auth import TokeModel
from app.models import UserResponseType, UserResponseTypeCreate


router = APIRouter(prefix="/user_response_type", tags=["user_response_type"])


@router.get(
    "",
    response_model=UserResponseType,
)
async def get_user_response_type(
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
    user_response_type_name: str = Query(description="UserResponseType name"),
) -> UserResponseType:
    service = UserResponseTypeService(token_model=token_model, session=session)
    return await service.get(user_response_type_name=user_response_type_name)


@router.post(
    "",
    response_model=UserResponseType,
)
async def create_user_response_type(
    data: UserResponseTypeCreate,
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
) -> UserResponseType:
    service = UserResponseTypeService(token_model=token_model, session=session)
    return await service.create(data=data)


@router.put(
    "",
    response_model=UserResponseType,
)
async def update_user_response_type(
    data: UserResponseTypeCreate,
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
    user_response_type_id: int = Query(description="UserResponseType ID", gt=0),
) -> UserResponseType:
    service = UserResponseTypeService(token_model=token_model, session=session)
    return await service.update(data=data, user_response_type_id=user_response_type_id)


@router.get(
    "/list",
    response_model=PaginatedUserResponseType,
)
async def get_user_response_type_list(
    request: Request,
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
    page_number: int = Query(description="Номер страницы в выдаче", default=1, ge=1),
    page_limit: int = Query(
        description="Кол-во обьектов на странице", default=10, ge=5
    ),
) -> PaginatedUserResponseType:
    service = UserResponseTypeService(token_model=token_model, session=session)
    pagination = PaginationService(request_url=request.url)
    return await service.list(
        page_number=page_number, page_limit=page_limit, service=pagination
    )


@router.delete("", response_model=KeyValueModel)
async def delete_user_response_type(
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
    user_response_type_name: str = Query(description="UserResponseType name"),
) -> KeyValueModel:
    service = UserResponseTypeService(token_model=token_model, session=session)
    return await service.delete(user_response_type_name=user_response_type_name)
