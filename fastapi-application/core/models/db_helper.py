from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (create_async_engine,
                                    AsyncEngine,
                                    AsyncSession,
                                    async_sessionmaker)

from core.config import settings


class DatabaseHelper:
    """
    Asynchronous database helper class for managing SQLAlchemy engine and sessions.

    This class provides an interface for creating and disposing of an async SQLAlchemy engine,
    as well as a convenient asynchronous session getter for use in dependency injection.

    Attributes:
        engine (AsyncEngine): The asynchronous SQLAlchemy engine.
        session_factory (async_sessionmaker[AsyncSession]): The asynchronous session factory.

    Example:
        ```python
        from core.db import db_helper

        async def my_function():
            async with db_helper.session_getter() as session:
                # Use the session here
                result = await session.execute(...)
        ```
    """
    def __init__(self,
                 url: str,
                 echo: bool = False,
                 echo_pool: bool = False,
                 pool_size: int = 5,
                 max_overflow: int = 10, ):
        pass
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Asynchronous generator that yields a database session.

        This method provides a convenient way to obtain a database session within an async context.
        The session is automatically closed when the context is exited.

        Yields:
            AsyncSession: An asynchronous database session.
        """
        async with self.session_factory() as session:
            yield session


db_helper = DatabaseHelper(
    url=str(settings.db.url),
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)
