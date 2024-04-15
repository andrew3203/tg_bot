"""Main project file"""

import logging
import logging.config

from fastapi import FastAPI, Request, status
from app.utils.exceptions import BaseException
from app.schema.exceptions import ExeptionData
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware
from app.routers.auth import router as auth_router
from app.routers.group import router as group_router
from app.routers.message import router as message_router
from app.routers.user import router as user_router
from config.settings import app_configs, settings

from .json import json

logging.config.fileConfig(settings.LOGGING_CONF_PATH, disable_existing_loggers=False)

logger = logging.getLogger(__name__)


app = FastAPI(default_response_class=ORJSONResponse, **app_configs)

json.set_fastapi_json()


@app.exception_handler(BaseException)
async def core_error_handler(request: Request, exc: BaseException) -> ORJSONResponse:
    if exc.code == status.HTTP_400_BAD_REQUEST:
        detail = "Произошел некорректный запрос. Попробуйте заново."
    elif exc.code == status.HTTP_403_FORBIDDEN:
        detail = "У вас нет доступа к ресурсу."
    elif exc.code == status.HTTP_404_NOT_FOUND:
        detail = "Обьект не найден."
    else:
        detail = f"Произошла внутренняя ошибка. Код: {exc.code}."

    model = ExeptionData(code=exc.code, msg=exc.msg, detail=detail)
    return ORJSONResponse(status_code=model.code, content=model.model_dump())


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=settings.CORS_HEADERS,
)


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, bool]:
    """healthcheck"""
    return {"status": True}


app.include_router(auth_router)
app.include_router(group_router)
app.include_router(message_router)
app.include_router(user_router)
