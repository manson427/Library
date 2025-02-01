import pytest_asyncio
from pathlib import Path
from alembic.command import upgrade, downgrade
from alembic.config import Config as AlembicConfig

from fastapi.testclient import TestClient
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.config import settings, AlembicTestData
from app.db.database import get_rep
from app.db.repositories.repository import Repository
from main import app

from app.api.utils.security import create_token
from datetime import timedelta


@pytest_asyncio.fixture(scope="session")
def engine():
    engine = create_async_engine(settings.DB_ALCHEMY_TEST.get_secret_value())
    yield engine
    engine.sync_engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def async_session_maker(engine):
    yield async_sessionmaker(engine, expire_on_commit=False)


@pytest_asyncio.fixture(scope="function")
async def get_db(async_session_maker):
    async with async_session_maker() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def override_get_rep(get_db):
    async def _override_get_rep() -> Repository:
        yield Repository(get_db)
    return _override_get_rep


@pytest_asyncio.fixture(scope="function")
async def client(override_get_rep) -> TestClient:
    app.dependency_overrides[get_rep] = override_get_rep
    return TestClient(app)


@pytest.fixture(scope="session")
def get_tokens():
    guest = None
    user_id2 = create_token(subject={"sub": str(2)}, expires_time=timedelta(minutes=settings.ACCESS_MINUTES))
    admin_id1 = create_token(subject={"sub": str(1)}, expires_time=timedelta(minutes=settings.ACCESS_MINUTES))
    user_id3 = create_token(subject={"sub": str(3)}, expires_time=timedelta(minutes=settings.ACCESS_MINUTES))
    user_id4 = create_token(subject={"sub": str(4)}, expires_time=timedelta(minutes=settings.ACCESS_MINUTES))
    user_id5 = create_token(subject={"sub": str(5)}, expires_time=timedelta(minutes=settings.ACCESS_MINUTES))
    user_id6 = create_token(subject={"sub": str(6)}, expires_time=timedelta(minutes=settings.ACCESS_MINUTES))
    user_fake = create_token(subject={"sub": str(666)}, expires_time=timedelta(minutes=settings.ACCESS_MINUTES))
    user_text = create_token(subject={"sub": 'text'}, expires_time=timedelta(minutes=settings.ACCESS_MINUTES))
    return {
        "guest": guest,
        "user_id2": user_id2,
        "admin_id1": admin_id1,
        "user_id3": user_id3,
        "user_id4": user_id4,
        "user_id5": user_id5,
        "user_id6": user_id6,
        "user_fake": user_fake,
        "user_text": user_text,
    }


@pytest.fixture(scope="session")
def alembic_config() -> AlembicConfig:
    project_dir = Path(__file__).parent.parent
    alembic_ini_path = Path.joinpath(project_dir.absolute(), "alembic.ini").as_posix()
    alembic_cfg = AlembicConfig(alembic_ini_path)
    migrations_dir_path = Path.joinpath(
        project_dir.absolute(), "app", "db", "alembic").as_posix()
    alembic_cfg.set_main_option("script_location", migrations_dir_path)
    alembic_cfg.set_main_option("sqlalchemy.url", settings.DB_ALCHEMY_TEST.get_secret_value())
    AlembicTestData.flag_test = True
    return alembic_cfg


@pytest_asyncio.fixture(scope="module")
def create(engine, alembic_config: AlembicConfig):
    upgrade(alembic_config, "head")
    yield engine
    downgrade(alembic_config, "base")


