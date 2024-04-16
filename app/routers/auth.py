from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_async_session
from app.schema.auth import AdminLoginModel, AdminSignupModel
from app.services.api.auth import auth_service


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/login",
    response_model=str,
    name="auth:login",
)
async def login(
    data: AdminLoginModel,
    session: AsyncSession = Depends(get_async_session),
) -> str:
    return await auth_service.login(data=data, session=session)


@router.post(
    "/signup",
    response_model=str,
    name="auth:login",
)
async def signup(
    data: AdminSignupModel,
    session: AsyncSession = Depends(get_async_session),
) -> str:
    return await auth_service.signup(data=data, session=session)
