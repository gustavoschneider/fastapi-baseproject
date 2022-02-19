# from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from .config import settings, CONNECT_ARGS

engine = create_async_engine(
    settings.database_url,
    echo=True,
    future=True,
    connect_args=CONNECT_ARGS
)

async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with async_session() as session:
        yield session
