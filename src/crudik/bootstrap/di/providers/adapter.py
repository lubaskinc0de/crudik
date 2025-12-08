from collections.abc import AsyncIterator

from dishka import AnyOf, Provider, Scope, WithParents, provide, provide_all
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from crudik.adapters.auth.auth_provider import SimpleAuthProvider
from crudik.adapters.auth.idp.auth_user import WebAuthUserIdProvider
from crudik.adapters.auth.idp.user import UserIdProviderImpl
from crudik.adapters.db.config import DbConfig
from crudik.adapters.db.gateway.auth_user import SAAuthUserGateway
from crudik.adapters.db.gateway.user import SAUserGateway
from crudik.application.common.uow import UoW


class AdapterProvider(Provider):
    """Dishka provider that registers all adapter implementations."""

    id_providers = provide_all(
        WithParents[WebAuthUserIdProvider],
        WithParents[UserIdProviderImpl],
        scope=Scope.REQUEST,
    )
    gateways = provide_all(
        WithParents[SAUserGateway],
        WithParents[SAAuthUserGateway],
        scope=Scope.REQUEST,
    )
    auth_provider = provide(WithParents[SimpleAuthProvider], scope=Scope.REQUEST)

    @provide(scope=Scope.APP)
    async def get_engine(self, config: DbConfig) -> AsyncIterator[AsyncEngine]:
        """Provides SQLAlchemy async engine instance with proper lifecycle management."""
        engine = create_async_engine(
            config.connection_url,
            future=True,
        )
        yield engine
        await engine.dispose()

    @provide(scope=Scope.APP)
    async def get_async_sessionmaker(
        self,
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        """Provides SQLAlchemy async session factory configured for the application."""
        session_factory = async_sessionmaker(
            engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )
        return session_factory

    @provide(scope=Scope.REQUEST)
    async def get_async_session(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> AsyncIterator[AnyOf[AsyncSession, UoW]]:
        """Provides a request-scoped database session that also implements the UoW protocol."""
        async with session_factory() as session:
            yield session
