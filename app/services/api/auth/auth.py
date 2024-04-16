from datetime import UTC, timedelta, datetime
from app.models import Admin
from sqlmodel.ext.asyncio.session import AsyncSession
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

from app.schema.auth import AdminLoginModel, AdminSignupModel
from .auth_jwt import auth_jwt_service
from sqlmodel import select
from app.utils.exceptions import AccessExeption, DataExeption


class AuthService:
    def __init__(self) -> None:
        self.exp_delta = timedelta(days=1)
        self.password_hasher = self.__load_password_hasher()
        self.iterations = 100000
        self.length = 32

    def __load_password_hasher(self) -> bytes:
        with open("password_hasher.key", "rb") as f:
            return f.read()

    async def _create_token(self, admin: Admin) -> str:
        return auth_jwt_service.encode_jwt(
            user_id=admin.id,  # type: ignore
            role="admin",
            exp_delta=timedelta(days=1),
        )

    async def _find_admin(self, email: str, session: AsyncSession) -> Admin | None:
        result = await session.exec(select(Admin).where(Admin.email == email))
        return result.one_or_none()

    async def _hash_password(self, plain_password: str, created_at: datetime) -> bytes:
        salt = str(created_at.replace(tzinfo=UTC).timestamp()).encode()
        input_key_material = self.password_hasher + plain_password.encode()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self.length,
            salt=salt,
            iterations=self.iterations,
            backend=default_backend(),
        )
        return kdf.derive(input_key_material)

    async def verify_password(self, plain_password: str, admin: Admin) -> bool:
        hash_password = await self._hash_password(
            plain_password=plain_password,
            created_at=admin.created_at,
        )
        return hash_password == admin.hashed_password

    async def login(self, data: AdminLoginModel, session: AsyncSession) -> str:
        admin = await self._find_admin(email=data.email, session=session)
        if admin is None:
            raise AccessExeption(msg="Пользователь не найден")
        if not await self.verify_password(plain_password=data.password, admin=admin):
            raise AccessExeption(msg="Неверный пароль")
        return await self._create_token(admin=admin)

    async def signup(self, data: AdminSignupModel, session: AsyncSession) -> str:
        now = datetime.now(UTC)
        hashed_password = await self._hash_password(
            plain_password=data.password,
            created_at=now,
        )
        admin = Admin(
            name=data.name,
            email=data.email,
            hashed_password=hashed_password,
            created_at=now,
        )
        if await self._find_admin(email=data.email, session=session) is not None:
            raise DataExeption(msg="Пользователь уже существует")
        session.add(admin)
        await session.commit()
        return await self._create_token(admin=admin)


auth_service = AuthService()
