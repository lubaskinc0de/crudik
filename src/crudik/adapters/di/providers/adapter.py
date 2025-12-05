from collections.abc import AsyncIterator

from bazario.asyncio import Dispatcher, Registry, Resolver
from bazario.asyncio.resolvers.dishka import DishkaResolver
from dishka import AnyOf, AsyncContainer, Provider, Scope, WithParents, provide, provide_all
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from crudik.adapters.auth.event_handlers import UserCreatedHandler
from crudik.adapters.auth.idp.auth_user import WebAuthUserIdProvider
from crudik.adapters.auth.idp.user import UserIdProviderImpl
from crudik.adapters.db.config import DbConfig
from crudik.adapters.db.gateway.auth_user import SAAuthUserGateway
from crudik.adapters.db.gateway.user import SAUserGateway
from crudik.application.common.event.user import UserCreated
from crudik.application.common.uow import UoW


class AdapterProvider(Provider):
    bazario_dispatcher = provide(WithParents[Dispatcher], scope=Scope.REQUEST)
    event_handlers = provide_all(
        UserCreatedHandler,
        scope=Scope.REQUEST,
    )
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

    @provide(scope=Scope.REQUEST)
    async def get_bazario_resolver(self, request_container: AsyncContainer) -> Resolver:
        return DishkaResolver(request_container)

    @provide(scope=Scope.APP)
    async def get_bazario_registry(self) -> Registry:
        registry = Registry()
        registry.add_notification_handlers(UserCreated, UserCreatedHandler)
        return registry
