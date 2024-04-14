"""Main project file"""

import logging
import logging.config

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware

from config.settings import app_configs, settings

from .json import json

logging.config.fileConfig(settings.LOGGING_CONF_PATH, disable_existing_loggers=False)

logger = logging.getLogger(__name__)


app = FastAPI(default_response_class=ORJSONResponse, **app_configs)

json.set_fastapi_json()

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
