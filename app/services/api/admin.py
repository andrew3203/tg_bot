from datetime import UTC, datetime
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models import Admin, AdminCreate
from app.schema.auth.token_model import TokeModel
from app.schema.base_model import KeyValueModel
from app.services.api.pagination import PaginationService
from app.schema.api import PaginatedAdmin
from app.utils.exceptions import AccessExeption
from .base import BaseModelService
from app.services.api.auth import auth_service, AuthService


class AdminService(BaseModelService):
    def __init__(
        self,
        token_model: TokeModel,
        session: AsyncSession,
        auth_service: AuthService = auth_service,
    ) -> None:
        super().__init__(token_model, session)
        self.auth_service = auth_service
        if not self.token_model.is_admin:
            raise AccessExeption(
                msg="У вас нету доступа к ресурсу, вы не администратор"
            )

    async def _validate_admin_access(self, admin_id: int | None = None) -> Admin:
        admin = await self._get(model=Admin, model_id=self.token_model.id)
        if not admin.is_superuser:
            if admin_id is not None and admin_id == self.token_model.id:
                return admin
            raise AccessExeption(
                msg="У вас нету доступа к ресурсу, вы не супер администратор"
            )
        return admin

    async def create(self, data: AdminCreate) -> Admin:
        await self._validate_admin_access()

        created = Admin.model_validate(data)
        created.created_at = datetime.now(UTC)
        created.hashed_password = await self.auth_service._hash_password(
            plain_password=data.hashed_password.decode(),
            created_at=created.created_at,
        )
        self.session.add(created)
        await self.session.commit()
        return created

    async def get(self, admin_id: int) -> Admin:
        await self._validate_admin_access(admin_id=admin_id)
        return await self._get(model=Admin, model_id=admin_id)

    async def update(self, data: AdminCreate, admin_id: int) -> Admin:
        await self._validate_admin_access(admin_id=admin_id)
        _admin = await self._get(model=Admin, model_id=admin_id)

        hashed_password = await self.auth_service._hash_password(
            plain_password=data.hashed_password.decode(),
            created_at=_admin.created_at,
        )
        if _admin.hashed_password != hashed_password:
            data.hashed_password = hashed_password

        await self.__set_params(model=_admin, data=data)
        self.session.add(_admin)
        await self.session.commit()
        return _admin

    async def delete(self, admin_id: int) -> KeyValueModel:
        await self._validate_admin_access(admin_id=admin_id)
        return await self._delete(model=Admin, model_id=admin_id)

    async def list(
        self, service: PaginationService, page_number: int = 1, page_limit: int = 10
    ) -> PaginatedAdmin:
        statement = select(Admin)
        try:
            await self._validate_admin_access()
        except AccessExeption:
            statement = select(Admin).where(Admin.id == self.token_model.id)
        return await self._list(
            schema=PaginatedAdmin,
            service=service,
            statement=statement,
            page_number=page_number,
            page_limit=page_limit,
        )
