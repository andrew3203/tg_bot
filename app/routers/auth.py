from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_async_session
from app.schema.auth import AdminLoginModel
from app.services.auth import auth_service


router = APIRouter()


@router.post(
    "/login",
    response_model=str,
    name="auth:login",
)
async def login(
    data: AdminLoginModel,
    session: AsyncSession = Depends(get_async_session),
) -> str:
    """
    A function to handle the login process for the authentication service.

    Parameters:
        - data: AdminLoginModel: The data containing the login information.

    Returns:
        - str: A string indicating the result of the login process.
    """
    return await auth_service.login(data=data, session=session)


@router.post(
    "/signup",
    response_model=str,
    name="auth:login",
)
async def signup(
    data: AdminLoginModel,
    session: AsyncSession = Depends(get_async_session),
) -> str:
    """
    A function to handle the signup process for the authentication service.

    Parameters:
        - data: AdminLoginModel: The data containing the login information.

    Returns:
        - str: A string indicating the result of the signup process.
    """
    return await auth_service.signup(data=data, session=session)
