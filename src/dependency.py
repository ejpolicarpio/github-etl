from fastapi import Depends
from src.configuration import Settings, get_settings as _get_settings
from src.database import DatabaseManager

async def get_settings() -> Settings:
    """get application settings"""
    return _get_settings(new=True)

async def get_db_manager() -> DatabaseManager:
    """get database manager"""
    settings = await get_settings()
    return DatabaseManager(settings)

async def get_initialized_db_manager(settings: Settings = Depends(get_settings)):
    """get initialized database manager"""
    db_manager = DatabaseManager(settings)
    if not db_manager.engine:
        await db_manager.initialize()
    return db_manager

