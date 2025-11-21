import asyncio
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import logging
from typing import List, Set, Dict
from urllib.parse import urljoin, urlparse
import concurrent.futures

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Crawler:
    def __init__(self, start_url: str, max_depth: int = 2, max_pages: int = 10):
        self.start_url = start_url
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.visited: Set[str] = set()
        self.results: List[Dict] = []
        self.base_domain = urlparse(start_url).netloc

    def is_valid_url(self, url: str) -> bool:
        parsed = urlparse(url)
        return parsed.netloc == self.base_domain and parsed.scheme in ['http', 'https']

    def is_doc_url(self, url: str) -> bool:
        # Accept all URLs from the same domain, exclude common non-doc patterns
        path = urlparse(url).path.lower()
        # Exclude certain patterns
        exclude_patterns = ['.jpg', '.png', '.gif', '.pdf', '.zip', '/cdn-cgi/']
        if any(pattern in path for pattern in exclude_patterns):
            return False
        # Accept everything else
        return True

    def _crawl_sync(self):
        """Synchronous crawl method to work around Windows asyncio issues"""
        logger.info(f"Starting sync crawl of {self.start_url}")
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context()
                
                # Queue: (url, depth)
                queue = [(self.start_url, 0)]
                
                while queue and len(self.visited) < self.max_pages:
                    url, depth = queue.pop(0)
                    
                    if url in self.visited or depth > self.max_depth:
                        continue
                    
                    self.visited.add(url)
                    logger.info(f"Crawling: {url} (Depth: {depth})")
                    
                    try:
                        page = context.new_page()
                        page.goto(url, wait_until="domcontentloaded", timeout=10000)
                        content = page.content()
                        
                        # Extract text
                        soup = BeautifulSoup(content, 'html.parser')
                        # Remove script and style elements
                        for script in soup(["script", "style"]):
                            script.decompose()
                        text = soup.get_text(separator='\n', strip=True)
                        
                        self.results.append({
                            "url": url,
                            "content": text,
                            "title": page.title()
                        })
                        
                        # Find links
                        if depth < self.max_depth:
                            links = page.query_selector_all("a")
                            for link in links:
                                href = link.get_attribute("href")
                                if href:
                                    absolute_url = urljoin(url, href)
                                    # Remove fragment
                                    absolute_url = absolute_url.split('#')[0]
                                    
                                    if (self.is_valid_url(absolute_url) and 
                                        absolute_url not in self.visited and
                                        self.is_doc_url(absolute_url)):
                                        queue.append((absolute_url, depth + 1))
                        
                        page.close()
                        
                    except Exception as e:
                        logger.error(f"Failed to crawl {url}: {e}")
                
                browser.close()
                logger.info(f"Crawl complete. Fetched {len(self.results)} pages.")
                return self.results
        except Exception as e:
            logger.error(f"Playwright failed: {e}", exc_info=True)
            raise

    async def crawl(self):
        """Async wrapper around sync crawl"""
        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = await loop.run_in_executor(executor, self._crawl_sync)
        return results

if __name__ == "__main__":
    # Test run
    import sys
    if len(sys.argv) > 1:
        url = sys.argv[1]
        crawler = Crawler(url)
        results = asyncio.run(crawler.crawl())
        print(f"Crawled {len(results)} pages.")
