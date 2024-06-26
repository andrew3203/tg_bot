"""Main project file"""
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
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
from app.routers.action import router as action_router
from app.routers.admin import router as admin_router
from app.routers.broadcast import router as broadcast_router
from app.routers.user_response_type import router as user_response_type_router
from app.routers.user_response import router as user_response_router
from app.routers.webhoks import router as webhoks_router
from config.settings import app_configs, settings
from app.bot.router import router as bot_router
from app.bot.app import setup_application
from .json import json

logging.config.fileConfig(settings.LOGGING_CONF_PATH, disable_existing_loggers=False)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    # Startup
    application = setup_application(is_webhook=settings.STAGE.is_deployed)
    await application.initialize()
    yield


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
    allow_origins=["*"],
    # allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=["*"],
)


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, bool]:
    """healthcheck"""
    return {"status": True}


app.include_router(auth_router)
app.include_router(group_router)
app.include_router(message_router)
app.include_router(user_router)
app.include_router(action_router)
app.include_router(admin_router)
app.include_router(broadcast_router)
app.include_router(user_response_type_router)
app.include_router(user_response_router)
app.include_router(bot_router)
app.include_router(webhoks_router)
