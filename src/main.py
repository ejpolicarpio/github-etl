from fastapi import FastAPI

from src.configuration import Settings, get_settings
from src.endpoints.repositories import router


def create_app(settings: Settings = None) -> FastAPI:
    settings = settings or get_settings(new=True)

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=f"{settings.BUILD_TAG}-{settings.BUILD_COMMIT}",
    )

    # Endpoints

    app.include_router(router, prefix="/api/v1")

    return app
