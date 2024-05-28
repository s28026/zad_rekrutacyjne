from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

DB_URL = "sqlite+aiosqlite:///./instance/db.sqlite3"

engine = create_async_engine(
    DB_URL,
    connect_args={"check_same_thread": False},
    echo=True,
)

Base = declarative_base()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session():
    session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with session() as session:
        try:
            yield session
        finally:
            await session.close()
