from session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from config import settings

# Créer l’engine PostgreSQL asynchrone
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Fabriquer les sessions
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Fonction pour initialiser les tables (option dev rapide)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
