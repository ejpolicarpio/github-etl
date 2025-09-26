from datetime import datetime

from src.configuration import Settings
from typing import List
import httpx

from src.database import DatabaseManager
from src.models import Repository
from src.schema import RepositoryResponseSchema
from sqlalchemy import select


class GitHubClient:
    def __init__(self, settings: Settings, db_manager: DatabaseManager = None):
        self.settings = settings
        self.db_manager = db_manager
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

                if self.db_manager:
                    await self._save_repository_to_db(item)

            return repositories

    async def _save_repository_to_db(self, repo_data: dict):
        try:
            async with self.db_manager.async_session() as session:
                stmt = select(Repository).where(Repository.full_name == repo_data.get("full_name"))
                existing = await session.scalar(stmt)

                if existing:
                    for key, value in repo_data.items():
                        if hasattr(existing, key):
                            setattr(existing, key, value)
                    existing.fetched_at = datetime.now()

                else:
                    repo_fields = {k: v for k, v in repo_data.items() if hasattr(Repository, k)}
                    repo = Repository(**repo_fields)
                    session.add(repo)

                await session.commit()
        except Exception as e:
            print(f"Error saving repository to database: {e}")

