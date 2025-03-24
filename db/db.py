from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.orm import declarative_base

from config import settings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL = settings.db.url
engine = create_async_engine(DATABASE_URL, echo=settings.db.echo, future=True)

Base = declarative_base()

_Session = async_sessionmaker(
    bind=engine,
    autoflush=False,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Функция для получения сессии."""
    async with _Session() as async_session:
        yield async_session
        await async_session.close()


@asynccontextmanager
async def get_async_context_session() -> AsyncGenerator[AsyncSession, None]:
    """Функция для получения сессии используя ее в контекстном менеджере."""
    async with _Session() as async_session:
        try:
            yield async_session
        finally:
            await async_session.close()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
