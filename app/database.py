from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool
from .config import settings

DATABASE_URL = "mysql+aiomysql://user:password@localhost/dbname"

engine = create_async_engine(
    settings.ASYNC_DATABASE_URL if hasattr(settings, 'ASYNC_DATABASE_URL') else DATABASE_URL,
    poolclass=AsyncAdaptedQueuePool,
    pool_size=settings.POOL_SIZE if hasattr(settings, 'POOL_SIZE') else 20,
    max_overflow=settings.MAX_OVERFLOW if hasattr(settings, 'MAX_OVERFLOW') else 30,
    pool_timeout=settings.POOL_TIMEOUT if hasattr(settings, 'POOL_TIMEOUT') else 30,
    pool_pre_ping=True,
    echo=False
)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()