from typing import Callable
from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.configuration import Settings, get_settings
from src.endpoints.repositories import router
from src.database import Base, DatabaseManager


def lifespan_provider(settings: Settings) -> Callable:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.db_manager = DatabaseManager(settings)
        await app.db_manager.initialize()

        async with app.db_manager.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield

        await app.db_manager.close()

    return lifespan


def create_app(settings: Settings = None) -> FastAPI:
    settings = settings or get_settings(new=True)
    lifespan = lifespan_provider(settings)

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=f"{settings.BUILD_TAG}-{settings.BUILD_COMMIT}",
        lifespan=lifespan,
    )

    # Endpoints

    app.include_router(router, prefix="/api/v1")

    return app
