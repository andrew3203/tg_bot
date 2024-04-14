from collections.abc import AsyncGenerator, Generator

import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession
from yarl import URL

from alembic.command import upgrade
from app.tests.utils import (
    alembic_config_from_url,
    from_sync_to_async_url_connection,
    tmp_database_url,
)
from config.settings import settings

from .database import get_async_session
from .main import app


@pytest.fixture(scope="session")
def test_db_url() -> URL:
    """
    Provides base PostgreSQL URL for creating temporary databases.
    """

    return URL(str(settings.SYNC_DATABASE_URL))


@pytest.fixture(scope="session")
def migrated_postgres_template(test_db_url) -> Generator[str, None, None]:
    """
    Creates temporary database and applies migrations.
    Database can be used as template to fast creation databases for tests.

    Has "session" scope, so is called only once per tests run.
    """
    with tmp_database_url(test_db_url, "template") as tmp_url:
        alembic_config = alembic_config_from_url(tmp_url)
        upgrade(alembic_config, "head")
        yield tmp_url


@pytest.fixture
def migrated_postgres(test_db_url: URL, migrated_postgres_template: str):
    """
    Quickly creates clean migrated database using temporary database as base.
    Use this fixture in tests that require migrated database.
    """
    template_db = URL(migrated_postgres_template).name
    with tmp_database_url(test_db_url, "pytest", template=template_db) as tmp_url:
        yield tmp_url


@pytest.fixture
async def postgres_async_engine(
    migrated_postgres: URL,
) -> AsyncGenerator[AsyncEngine, None]:
    url = from_sync_to_async_url_connection(str(migrated_postgres))
    engine = create_async_engine(url, echo=True)

    try:
        yield engine
    finally:
        await engine.dispose()


@pytest.fixture
def sync_session(migrated_postgres: str) -> Generator[Session, None, None]:
    engine = create_engine(str(migrated_postgres))
    session_maker = sessionmaker(
        engine,
        class_=Session,
        expire_on_commit=False,
        autocommit=False,
        autoflush=True,
    )

    with session_maker() as session:
        try:
            yield session
        finally:
            session.close()


@pytest.fixture()
async def async_session(
    postgres_async_engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    async_session_maker = sessionmaker(
        bind=postgres_async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )  # type: ignore
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


@pytest.fixture()
async def mock_async_session(
    async_session: AsyncSession,
) -> AsyncGenerator[AsyncSession, None]:
    app.dependency_overrides[get_async_session] = lambda: async_session
    yield async_session
    app.dependency_overrides = {}


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
