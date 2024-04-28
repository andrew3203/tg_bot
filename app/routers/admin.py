from typing import Annotated
from fastapi import APIRouter, Depends, Query, Request
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_async_session
from app.schema.api import PaginatedAdmin
from app.schema.base_model import KeyValueModel
from app.services.api import PaginationService, AdminService
from app.services.api.auth import get_current_user
from app.schema.auth import TokeModel
from app.models import Admin, AdminCreate


router = APIRouter(prefix="/admin", tags=["admin"])


@router.get(
    "",
    response_model=Admin,
)
async def get_admin(
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
    admin_id: int = Query(description="Admin ID", gt=0),
) -> Admin:
    service = AdminService(token_model=token_model, session=session)
    return await service.get(admin_id=admin_id)


@router.post(
    "",
    response_model=Admin,
)
async def create_admin(
    data: AdminCreate,
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
) -> Admin:
    service = AdminService(token_model=token_model, session=session)
    return await service.create(data=data)


@router.put(
    "",
    response_model=Admin,
)
async def update_admin(
    data: AdminCreate,
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
    admin_id: int = Query(description="Admin ID", gt=0),
) -> Admin:
    service = AdminService(token_model=token_model, session=session)
    return await service.update(data=data, admin_id=admin_id)


@router.get(
    "/list",
    response_model=PaginatedAdmin,
)
async def get_admin_list(
    request: Request,
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
    page_number: int = Query(description="Номер страницы в выдаче", default=1, ge=1),
    page_limit: int = Query(
        description="Кол-во обьектов на странице", default=10, ge=5
    ),
) -> PaginatedAdmin:
    service = AdminService(token_model=token_model, session=session)
    pagination = PaginationService(request_url=request.url)
    return await service.get_list(
        page_number=page_number, page_limit=page_limit, service=pagination
    )


@router.delete("", response_model=KeyValueModel)
async def delete_admin(
    token_model: Annotated[TokeModel, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
    admin_id: int = Query(description="Admin ID", gt=0),
) -> KeyValueModel:
    service = AdminService(token_model=token_model, session=session)
    return await service.delete(admin_id=admin_id)
