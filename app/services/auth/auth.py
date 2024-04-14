from datetime import timedelta
from app.models import Admin
from sqlmodel.ext.asyncio.session import AsyncSession
from cryptography.fernet import Fernet

from app.schema.auth import AdminLoginModel
from .auth_jwt import auth_jwt_service
from sqlmodel import select
from app.utils.exceptions import AccessExeption, DataExeption


class AuthService:
    def __init__(self) -> None:
        self.exp_delta = timedelta(days=1)
        self.password_hasher = self.__load_password_hasher()

    def __load_password_hasher(self) -> bytes:
        with open("password_hasher.key", "rb") as f:
            return f.read()

    async def _create_token(self, admin: Admin) -> str:
        return auth_jwt_service.encode_jwt(
            user_id=admin.id,
            role="admin",
            exp_delta=timedelta(days=1),
        )

    async def _find_admin(self, email: str, session: AsyncSession) -> Admin | None:
        result = await session.exec(select(Admin).where(Admin.email == email))
        return result.one_or_none()

    async def _hash_password(self, plain_password: str) -> bytes:
        return Fernet(self.password_hasher).encrypt(plain_password.encode())

    async def verify_password(self, plain_password: str, admin: Admin) -> bool:
        origin_hash_password = self._hash_password(plain_password=plain_password)
        return origin_hash_password == admin.hashed_password

    async def login(self, data: AdminLoginModel, session: AsyncSession) -> str:
        admin = await self._find_admin(email=data.email, session=session)
        if admin is None:
            raise AccessExeption(msg="Пользователь не найден")
        if not await self.verify_password(data.password, admin):
            raise AccessExeption(msg="Неверный пароль")
        return await self._create_token(admin=admin)

    async def signup(self, data: AdminLoginModel, session: AsyncSession) -> str:
        hashed_password = await self._hash_password(plain_password=data.password)
        admin = Admin(email=data.email, hashed_password=hashed_password)
        if await self._find_admin(email=data.email, session=session) is not None:
            raise DataExeption(msg="Пользователь уже существует")
        session.add(admin)
        await session.commit()
        return await self._create_token(admin=admin)


auth_service = AuthService()
