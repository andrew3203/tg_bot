"""
Main Config File of the project
"""

from typing import Any

from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings

from config.constants import Stage


class Config(BaseSettings):
    """
    Contains env config varibels of the project
    """

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    REDIS_URL: RedisDsn

    STAGE: Stage = Stage.LOCAL

    LOGGING_CONF_PATH: str

    CORS_ORIGINS: list[str]
    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: list[str]

    SITE_DOMAIN: str = "8000"
    TELEGRAM_BOT_TOKEN: str = "12345678"
    TELEGRAM_BOT_WEBHOOK_SECRET: str = "supersecret"
    LOGS_CHAT_ID: int

    APP_VERSION: str = "1.0.0"

    S3_BUCKET: str
    S3_KEY_ID: str
    S3_KEY: str
    S3_REGION_NAME: str
    S3_DOMAIN: str

    @classmethod
    def _allowed_hosts_list(cls, value: str) -> list[str]:
        return [host.strip() for host in value.split(",")]

    @property
    def DEBUG(self):
        return self.STAGE == Stage.LOCAL

    @property
    def SYNC_DATABASE_URL(self) -> PostgresDsn:
        url: PostgresDsn = PostgresDsn(
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
        return url

    @property
    def ASYNC_DATABASE_URL(self) -> PostgresDsn:
        url: PostgresDsn = PostgresDsn(
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
        return url


settings = Config()  # type: ignore

app_configs: dict[str, Any] = {
    "title": "app API",
    "version": settings.APP_VERSION,
    "debug": settings.DEBUG,
}
if settings.STAGE.is_deployed:
    app_configs["root_path"] = f"/v{settings.APP_VERSION}"

if not settings.STAGE.is_debug:
    app_configs["openapi_url"] = None  # hide docs
