import os
from collections.abc import AsyncIterable, AsyncIterator

import aiohttp
import pytest
from aiohttp import ClientSession
from dishka import AsyncContainer
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from crudik.adapters.api_client import APIClient, APIClientConfig
from crudik.bootstrap.config.loader import Config
from crudik.bootstrap.di.container import get_async_container


@pytest.fixture
async def app_config() -> Config:
    """Load and provide app config."""
    return Config.load()


@pytest.fixture
async def container() -> AsyncIterator[AsyncContainer]:
    """Create and provide async DI container for tests."""
    container = get_async_container(Config.load())
    yield container
    await container.close()


@pytest.fixture
async def session(container: AsyncContainer) -> AsyncIterator[AsyncSession]:
    """Create and provide database session for tests."""
    async with container() as r:
        yield (await r.get(AsyncSession))


@pytest.fixture(autouse=True)
async def gracefully_teardown(
    session: AsyncSession,
) -> AsyncIterable[None]:
    """Automatically truncate all tables after each test."""
    yield
    await session.execute(
        text("""
            DO $$
            DECLARE
                tb text;
            BEGIN
                FOR tb IN (
                    SELECT tablename
                    FROM pg_catalog.pg_tables
                    WHERE schemaname = 'public'
                      AND tablename != 'alembic_version'
                )
                LOOP
                    EXECUTE 'TRUNCATE TABLE ' || tb || ' CASCADE';
                END LOOP;
            END $$;
        """),
    )
    await session.commit()


@pytest.fixture
async def http_session(base_url: str) -> AsyncIterator[ClientSession]:
    """Create and provide HTTP client session for API tests."""
    async with aiohttp.ClientSession(base_url=base_url) as session:
        yield session


@pytest.fixture
def base_url() -> str:
    """Get API base URL from environment variable."""
    return os.environ["API_URL"]


@pytest.fixture
def api_client(http_session: ClientSession, app_config: Config) -> APIClient:
    """Create and provide API client for tests."""
    return APIClient(
        session=http_session,
        config=APIClientConfig(
            auth_user_id_header=app_config.web_auth_user_id_provider.user_id_header,
        ),
    )
