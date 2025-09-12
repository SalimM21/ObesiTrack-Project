from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings


DATABASE_URL = settings.DATABASE_URL
# Ensure async driver for PostgreSQL if using psycopg2
if DATABASE_URL.startswith("postgresql+psycopg2"):
    DATABASE_URL = DATABASE_URL.replace("postgresql+psycopg2", "postgresql+asyncpg")

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False, future=True)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autoflush=False, autocommit=False
)

Base = declarative_base()

async def init_db():
    async with engine.begin() as conn:
        from app.db import models  # noqa: F401 - ensure models are imported for metadata
        await conn.run_sync(Base.metadata.create_all)