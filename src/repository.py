from src.configuration import Settings
from typing import List
import httpx

from src.schema import RepositoryResponseSchema


class GitHubClient:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "github-etl/1.0",
        }

    async def search_repositories(self, query: str) -> List[RepositoryResponseSchema]:
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}/search/repositories"
            params = {"q": query}

            response = await client.get(url, headers=self.headers, params=params)
            response.raise_for_status()

            data = response.json()
            repositories = []
            for item in data.get("items", []):
                repo = RepositoryResponseSchema(**item)
                repositories.append(repo)
            return repositories
