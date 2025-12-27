import os
from collections.abc import AsyncIterable, AsyncIterator
from uuid import uuid4

import aiohttp
import jwt
import pytest
from aiohttp import ClientSession
from dishka import AsyncContainer
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from crudik.adapters.api_client import APIClient, APIClientConfig
from crudik.adapters.tracing import TraceId
from crudik.main.config.loader import Config, get_toml_config_path, load_config_from_toml
from crudik.main.di.container import get_async_container

# This is a fake private key used only to sign fake access token for tests
DUMMY_PRIVATE_KEY = """
-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDEGaNRi4y3Aneo
kMONcleALP0h2SPEr4Wqj0Bzu3/VEQfhcuMKtWqQenx/wZ1kYlr1NAZUYFxP0VE6
pqlt6x9NGzgaUyp8x/S5jVPjxrcMsq+N+zwES6zrMpTbjJgA6eWlZ50amAgwtVvP
/aUUll6SckDCWpq51Xu/tmMm/uTdPaT/loBVoEfluqLLq4qcqROwnqtOZs/0aTFx
w76tOqsBl+QtaRCoU5XRHgS+Mf0KuMh+mktelDsTEDCyu4cDn5viTQ8C7b5oChbn
lSaPq52aQ3tsrp/3HixW7E2y3d58tIUV+X6/5drdf+QgysNELNO6H/0n+4aXc6DM
MqspZs2DAgMBAAECggEAEYyd0glkEWi2Hq694WWvMPhVuva8vbhbhPUG9pR8DyxU
ATgP24B6xe1AQQqptDcdHr6GJnztJfN8inwpw318MqFR9wEkV0BpxUVBkavR69/9
1/341AWVtwKy0acWX1aPR6srIxsh+IHycn2njV0bn418ACitmh3h0jlXTEEZaDcY
0BlE/eda3yRBO1yIyk1LIFqIotQyEm0eJtuQQX6HlWbGsuBRjCKAI5qhVuxMmVEa
YZVag+Ko0IKjDQxtIH1kLsadMX6/G6p8KO4RZgwsDk7eyR0ISvuCsDb2H2SZDGg6
Zt1uAmxgWTF1RqypAaq/tJN4VXrtI3k61uvo0HwiAQKBgQD0nLUnn9hKR40gF6oN
x+XBWB/CrILDnXKNnfzsf/TLC5t8wHp06lo9kNJKcc3AKXlGU0ikvnYJwJYDVeKG
6V+y3vphS8gGRAg2yI/P9wBOUKvioJyfC04/rZ1SiSZpQUHs2jzgErqFKQqXpCzB
yPYULwhxaCfMG9aXQTIaze3SgwKBgQDNOsNxc40H8OL8Xnbla7JeA+tVK8jb/k30
taC17v7a22Nd+Ao4M/+H6ToCQEXhD0RSsWtmO6ys4mlCuH0+N+h++5sjCd1HmJxm
UrDoP0uVXc4F1R0SmSZoMwkg3Co8I7DNb+eINCh2xAybynIb6w1736HJE/h0JbJS
/0sgpJYpAQKBgQDjmJNtpOqoYl7LB3mwjNgXx5j1l3Gr9OlLHz7gBkaMTeaEcsr9
0bfZJNCld7ILJAu1BXTH5HcLp+dsfxLgmG/0jEfHE62vNsm1v3Mf+yCLvb/Qg8R2
rxxFX5LL4tSchp2CdaTCkGp/z6oNYjJKtGNScFiYvGKbJSPLZFvsWML5ZQKBgB/g
J6kAXIBGPssZ1PevMYX+r9eLtGfO6MbASxTW6QiPGLDorJWsJd0zMUpWN0RMfb0m
R1sam6hChjzRsMowHtFSPPdFOfQ71NbjswxvgErTxgML5bcUyG1Yt+s9puWuWXCf
F+QEzeAcdSThXbXOXUrHIja7/lPz4u2XL1EDnzsBAoGBAJOinUr0t3nUEKhKcqJ9
gJWzg5NcCJa53leWAceA2fpttF2GgEYsR6udisqYI+UH1TUaMrujUqGFbNqXqdHo
7QGJZoHc7/RNeQ14u0SDY37QmyzgMt8/4enn6O4IzMML+b6cDi+khx6dc2NEUu+F
6p95hLlC0FKt9LZYt2jHi5O9
-----END PRIVATE KEY-----
"""


@pytest.fixture
async def app_config() -> Config:
    """Load and provide app config."""
    return load_config_from_toml(get_toml_config_path())


@pytest.fixture
async def trace_id() -> TraceId:
    """Generate trace id."""
    return uuid4().hex


@pytest.fixture
async def container(app_config: Config) -> AsyncIterator[AsyncContainer]:
    """Create and provide async DI container for tests."""
    container = get_async_container(app_config)
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
async def access_token(app_config: Config) -> str:
    """Dummy access token with email_verified set to True."""
    return jwt.encode(
        {
            "email_verified": True,
        },
        key=DUMMY_PRIVATE_KEY,
        algorithm=app_config.web_auth.access_token_alg,
    )


@pytest.fixture
def api_client(http_session: ClientSession, app_config: Config, trace_id: TraceId, access_token: str) -> APIClient:
    """Create and provide API client for tests."""
    return APIClient(
        session=http_session,
        config=APIClientConfig(
            auth_user_id_header=app_config.web_auth.user_id_header,
            access_token_header=app_config.web_auth.access_token_header,
        ),
        trace_id=trace_id,
        tracing_config=app_config.tracing,
        access_token=access_token,
    )
