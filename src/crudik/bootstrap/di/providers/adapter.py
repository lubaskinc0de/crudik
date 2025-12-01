from collections.abc import AsyncIterator

from dishka import AnyOf, Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from crudik.adapters.db.config import DbConfig
from crudik.application.common.uow import UoW


class AdapterProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_engine(self, config: DbConfig) -> AsyncIterator[AsyncEngine]:
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
        async with session_factory() as session:
            yield session
