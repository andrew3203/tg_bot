from typing import TypeVar
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schema.auth import TokeModel
from app.schema.base_model import KeyValueModel
from sqlmodel import select
from app.utils.exceptions import NotFoundException
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import SelectOfScalar
from .pagination import PaginationService, PaginatedData

Model = TypeVar("Model", bound=SQLModel)
T = TypeVar("T", bound=SQLModel)


class BaseModelService:
    def __init__(self, token_model: TokeModel, session: AsyncSession) -> None:
        self.token_model = token_model
        self.session = session

    async def _set_params(self, model: Model, data: T) -> Model:
        for field in model.model_fields:
            if hasattr(data, field):
                setattr(model, field, getattr(data, field))
        return model

    async def _create(self, data: T, model: type[Model]) -> Model:
        created = model(**data.model_dump())
        self.session.add(created)
        await self.session.commit()
        return created

    async def _get(self, model: type[Model], model_id: int) -> Model:
        result = await self.session.exec(select(model).where(model.id == model_id))  # type: ignore
        _model = result.one_or_none()
        if _model is None:
            raise NotFoundException(msg="Обьект не найден")
        return _model

    async def _update(self, model: type[Model], model_id: int, data: T) -> Model:
        _model = await self._get(model=model, model_id=model_id)
        await self._set_params(model=_model, data=data)
        self.session.add(_model)
        await self.session.commit()
        return _model

    async def _delete(self, model: type[Model], model_id: int) -> KeyValueModel:
        _model = await self._get(model=model, model_id=model_id)
        await self.session.delete(_model)
        await self.session.commit()
        return KeyValueModel(key="OK", value="Обьект удален")

    async def _list(
        self,
        schema: type[PaginatedData],
        service: PaginationService,
        statement: SelectOfScalar,
        page_number: int = 1,
        page_limit: int = 10,
    ) -> PaginatedData:
        result = await self.session.exec(statement)
        data = result.all()
        return await service.list(
            data=data,
            schema=schema,
            count=len(data),
            page_number=page_number,
            page_limit=page_limit,
        )
