"""
Jina AI web scraping service using Jina Reader API.

Provides fast, clean web scraping without browser automation.
"""

import httpx
from typing import Optional, Dict
import logging
import os
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class JinaScraper:
    """Web scraper using Jina AI Reader API."""
    
    BASE_URL = "https://r.jina.ai"
    
    def __init__(self):
        self.api_key = os.getenv("JINA_API_KEY")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "X-Return-Format": "markdown"
        } if self.api_key else {"X-Return-Format": "markdown"}
    
    async def scrape(self, url: str, timeout: int = 30) -> Dict[str, str]:
        """
        Scrape a URL and return clean markdown content.
        
        Args:
            url: The URL to scrape
            timeout: Request timeout in seconds
            
        Returns:
            Dict with 'content' (markdown), 'title', and 'url'
            
        Raises:
            httpx.HTTPError: If scraping fails
        """
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                jina_url = f"{self.BASE_URL}/{url}"
                logger.info(f"🕷️  Scraping {url} via Jina Reader...")
                
                response = await client.get(jina_url, headers=self.headers)
                response.raise_for_status()
                
                content = response.text
                
                # Extract title from first H1 if present
                title = url.split("/")[-1] or url
                if content.startswith("# "):
                    title = content.split("\n")[0].replace("# ", "").strip()
                
                logger.info(f"✅ Scraped {len(content)} characters from {url}")
                
                return {
                    "content": content,
                    "title": title,
                    "url": url,
                    "source": "website"
                }
                
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 402:
                logger.warning(f"⚠️  Jina API quota exceeded, falling back to basic HTTP scraper")
                return await self._fallback_scrape(url, timeout)
            else:
                logger.error(f"❌ Failed to scrape {url}: {e}")
                raise
        except httpx.HTTPError as e:
            logger.error(f"❌ Failed to scrape {url}: {e}")
            raise
    
    async def _fallback_scrape(self, url: str, timeout: int = 30) -> Dict[str, str]:
        """Fallback scraper using basic HTTP when Jina fails."""
        try:
            async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
                logger.info(f"📄 Using basic HTTP scraper for {url}...")
                response = await client.get(url)
                response.raise_for_status()
                
                content = response.text
                
                # Basic title extraction
                title = url.split("/")[-1] or "Document"
                if "<title>" in content:
                    start = content.find("<title>") + 7
                    end = content.find("</title>", start)
                    if end > start:
                        title = content[start:end].strip()
                
                logger.info(f"✅ Fetched {len(content)} characters (basic HTTP)")
                
                return {
                    "content": content,
                    "title": title,
                    "url": url,
                    "source": "website"
                }
        except Exception as e:
            logger.error(f"❌ Fallback scraper failed: {e}")
            raise

    
    async def scrape_multiple(self, urls: list[str]) -> list[Dict[str, str]]:
        """
        Scrape multiple URLs concurrently.
        
        Args:
            urls: List of URLs to scrape
            
        Returns:
            List of scraping results
        """
        import asyncio
        
        tasks = [self.scrape(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out errors
        successful = [r for r in results if not isinstance(r, Exception)]
        failed = [r for r in results if isinstance(r, Exception)]
        
        if failed:
            logger.warning(f"⚠️  {len(failed)} URLs failed to scrape")
        
        return successful
