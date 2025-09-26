from fastapi import FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # GitHub API settings
    github_owner: str | None = None
    github_repo: str | None = None
    user_agent: str | None = None
    api_base: str | None = None
    api_version: str | None = None
    timeout_sec: int | None = None

    # Database settings
    database_username: str = "user"
    database_password: str = "password"
    database_host: str = "localhost"
    database_port: int = 5432
    database_name: str = "github_etl"
    database_echo: bool = True # set to false in production

    # App Settings
    PROJECT_NAME: str = "GitHub ETL"
    BUILD_TAG: str = "dev"
    BUILD_COMMIT: str = "local"


def get_settings(runtime=None, new=False) -> Settings:
    if new:
        return Settings()

    if isinstance(runtime, FastAPI):
        return runtime.settings
    return runtime.app.settings
