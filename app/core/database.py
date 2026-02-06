from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

# 1. Create the engine (Note: No 'create_async_session' here)
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
)

# 2. Create the session factory
async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 3. Use a base class for your models
class Base(DeclarativeBase):
    pass
 
# 4. The dependency for your routes
async def get_db():
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()