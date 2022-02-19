import pytest
import pytest_asyncio

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.config import settings, CONNECT_ARGS
from app.main import app
from app.database import get_session

engine = create_async_engine(
    settings.database_url,
    echo=True,
    future=True,
    connect_args=CONNECT_ARGS
)

async def override_get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture
async def test_db():
    async with engine.connect() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


@pytest.fixture
def client() -> TestClient:
    app.dependency_overrides[get_session] = override_get_session
    return TestClient(app)
