import httpx
import base64
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class GitHubFetcher:
    def __init__(self, repo_url: str, token: Optional[str] = None):
        self.repo_url = repo_url
        self.token = token
        self.owner, self.repo = self._parse_url(repo_url)
        self.base_url = f"https://api.github.com/repos/{self.owner}/{self.repo}"
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        if token:
            self.headers["Authorization"] = f"Bearer {token}"

    def _parse_url(self, url: str):
        # Expected format: https://github.com/owner/repo
        parts = url.rstrip('/').split('/')
        return parts[-2], parts[-1]

    async def fetch_file(self, path: str) -> Optional[str]:
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}/contents/{path}"
            logger.info(f"Fetching file: {url}")
            resp = await client.get(url, headers=self.headers)
            
            if resp.status_code == 200:
                data = resp.json()
                if isinstance(data, dict) and data.get('type') == 'file':
                    content = base64.b64decode(data['content']).decode('utf-8')
                    return content
            else:
                logger.warning(f"Failed to fetch {path}: {resp.status_code}")
            return None

    async def fetch_commits(self, limit: int = 20) -> List[Dict]:
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}/commits?per_page={limit}"
            resp = await client.get(url, headers=self.headers)
            if resp.status_code == 200:
                return resp.json()
            return []

    async def fetch_repo_structure(self, path: str = "") -> List[Dict]:
        # Recursive fetch could be expensive, for prototype we might just fetch root docs
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}/contents/{path}"
            resp = await client.get(url, headers=self.headers)
            if resp.status_code == 200:
                return resp.json()
            return []

if __name__ == "__main__":
    # Test
    import asyncio
    async def main():
        fetcher = GitHubFetcher("https://github.com/fastapi/fastapi")
        readme = await fetcher.fetch_file("README.md")
        if readme:
            print(f"README length: {len(readme)}")
        
    asyncio.run(main())
