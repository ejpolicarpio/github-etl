from fastapi import APIRouter, Depends
from src.repository import GitHubClient
from src.configuration import Settings, get_settings
from src.schema import RepositoryResponseSchema
from typing import List

router = APIRouter()

DEFAULT_TAG = "Repositories"


@router.get(
    "/search", response_model=List[RepositoryResponseSchema], tags=[DEFAULT_TAG]
)
async def search_repositories(
    query: str = "stars:>1000", settings: Settings = Depends(get_settings)
):
    client: GitHubClient = GitHubClient(settings=settings)
    return await client.search_repositories(query)
