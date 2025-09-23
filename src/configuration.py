from fastapi import FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    github_owner: str | None = None
    github_repo: str | None = None
    user_agent: str | None = None
    api_base: str | None = None
    api_version: str | None = None
    timeout_sec: int | None = None


def get_settings(runtime: FastAPI = None, new=False) -> Settings:
    if new:
        return Settings()

    if isinstance(runtime, FastAPI):
        return runtime.settings
    return runtime.app.settings
