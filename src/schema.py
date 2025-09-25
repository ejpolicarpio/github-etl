from datetime import datetime

from pydantic import BaseModel


class RepositoryResponseSchema(BaseModel):
    model_config = {"extra":"ignore"}

    id: int | None = None
    name: str | None = None
    full_name: str | None = None
    description: str | None = None
    stargazers_count: int | None = None
    watchers_count: int | None = None
    forks_count: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    html_url: str | None = None
    language: str | None = None
