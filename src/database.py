from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from src.configuration import Settings


class Base(DeclarativeBase):
    pass


class DatabaseManager:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.engine = None
        self.async_session = None

    def get_database_url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.settings.database_username}:{self.settings.database_password}"
            f"@{self.settings.database_host}:{self.settings.database_port}"
            f"/{self.settings.database_name}"
        )

    async def initialize(self):
        self.engine = create_async_engine(self.get_database_url(), echo=self.settings.database_echo)
        self.async_session = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def get_session(self) -> AsyncSession:
        async with self.async_session() as session:
            yield session

    async def close(self):
        if self.engine:
            await self.engine.dispose()


db_manager = DatabaseManger(None)
