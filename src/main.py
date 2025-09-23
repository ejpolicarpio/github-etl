from fastapi import FastAPI

from src.configuration import Settings, get_settings


def create_app(settings: Settings = None) -> FastAPI:
    settings = settings or get_settings(new=True)

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=f"{settings.BUILD_TAG}-{settings.BUILD_COMMIT}",
    )

    app.settings = settings

    # Endpoints

    app.include_router(
        prefix="",
    )

    return app
