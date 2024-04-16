from typing import Annotated
from fastapi import APIRouter, Depends, Query, Request
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_async_session
from app.schema.api import PaginatedUser
from app.schema.base_model import KeyValueModel
from app.services.api import PaginationService, UserService
from app.services.api.auth import get_current_user
from app.schema.auth import TokeModel
from app.models import User, UserCreate


router = APIRouter(prefix="/user", tags=["user"])


@router.get(
    "",
    response_model=User,
)
async def get_user(
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
    user_id: int = Query(description="User ID", gt=0),
) -> User:
    service = UserService(token_model=token_model, session=session)
    return await service.get(user_id=user_id)


@router.post(
    "",
    response_model=User,
)
async def create_user(
    data: UserCreate,
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
) -> User:
    service = UserService(token_model=token_model, session=session)
    return await service.create(data=data)


@router.put(
    "",
    response_model=User,
)
async def update_user(
    data: UserCreate,
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
    user_id: int = Query(description="User ID", gt=0),
) -> User:
    service = UserService(token_model=token_model, session=session)
    return await service.update(data=data, user_id=user_id)


@router.get(
    "/list",
    response_model=PaginatedUser,
)
async def get_user_list(
    request: Request,
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
    page_number: int = Query(description="Номер страницы в выдаче", default=1, ge=1),
    page_limit: int = Query(
        description="Кол-во обьектов на странице", default=10, ge=5
    ),
) -> PaginatedUser:
    service = UserService(token_model=token_model, session=session)
    pagination = PaginationService(request_url=request.url)
    return await service.list(
        page_number=page_number, page_limit=page_limit, service=pagination
    )


@router.delete("", response_model=KeyValueModel)
async def delete_user(
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
    user_id: int = Query(description="User ID", gt=0),
) -> KeyValueModel:
    service = UserService(token_model=token_model, session=session)
    return await service.delete(user_id=user_id)
