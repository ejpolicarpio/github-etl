from fastapi import APIRouter, Depends

from src.dependency import get_settings, get_initialized_db_manager
from src.repository import GitHubClient
from src.schema import RepositoryResponseSchema
from typing import List

router = APIRouter()

DEFAULT_TAG = "Repositories"


@router.get(
    "/search", response_model=List[RepositoryResponseSchema], tags=[DEFAULT_TAG]
)
async def search_repositories(
    query: str = "stars:>1000",
    settings = Depends(get_settings),
    db_manager=Depends(get_initialized_db_manager),
):
    client: GitHubClient = GitHubClient(settings=settings, db_manager=db_manager)
    return await client.search_repositories(query)
