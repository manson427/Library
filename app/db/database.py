from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.config import settings

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.repository import Repository

from fastapi import Depends

engine = create_async_engine(
    url=settings.DB_ALCHEMY.get_secret_value(),
    echo=settings.DB_ECHO
)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        yield session

async def get_rep(session: AsyncSession = Depends(get_db)) -> Repository:
    res = Repository(session)
    return res