from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    github_owner: str | None
    github_repo: str | None
    user_agent: str | None
    api_base: str | None
    api_version: str | None
    timeout_sec: int = 20

settings = Settings()





