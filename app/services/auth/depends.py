import logging
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import APIKeyHeader
from pydantic import ValidationError

from app.schema.exceptions import ExeptionData
from app.schema.auth.token_model import TokeModel
from .auth_jwt import auth_jwt_service


# Определение схемы авторизации
class KFPAPIKeyHeader(APIKeyHeader):
    async def __call__(self, request: Request) -> str | None:
        api_key = request.headers.get(self.model.name)
        if not api_key:
            if self.auto_error:
                model = ExeptionData(
                    code=status.HTTP_401_UNAUTHORIZED,
                    msg="Ошибка авторизации. Данные для авторизации не предоставлены.",
                    detail="Ошибка авторизации.",
                )
                raise HTTPException(status_code=model.code, detail=model.model_dump())
            else:
                return None
        return api_key


api_header_scheme = KFPAPIKeyHeader(name="token")


async def get_current_user(token: Annotated[str, Depends(api_header_scheme)]):
    try:
        jwt = auth_jwt_service.decode_jwt(token=token)
    except Exception as why:
        model = ExeptionData(
            code=status.HTTP_401_UNAUTHORIZED,
            msg=f"Ошибка в проверку токена: {str(why)}",
            detail="Ошибка авторизации.",
        )
        raise HTTPException(status_code=model.code, detail=model.model_dump())

    try:
        logging.error(f"jwt: {jwt}")
        user = TokeModel.model_validation(jwt)
    except ValidationError as why:
        model = ExeptionData(
            code=status.HTTP_401_UNAUTHORIZED,
            msg=f"Ошибка авторизации: {str(why)}",
            detail="Ошибка авторизации.",
        )
        raise HTTPException(status_code=model.code, detail=model.model_dump())

    if not user.is_admin:
        model = ExeptionData(
            code=status.HTTP_403_FORBIDDEN,
            msg="Пользователь не имеет необходимого тарифа или потока для доступа к КФП.",
            detail="У вас нету доступа к ресурсу.",
        )
        raise HTTPException(status_code=model.code, detail=model.model_dump())
    return user
