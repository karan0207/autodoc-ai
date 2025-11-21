import sys
import asyncio
sys.path.insert(0, 'c:/crawler')

from backend.crawler.crawler import Crawler

async def test():
    crawler = Crawler("https://www.firecrawl.dev/", max_pages=3)
    results = await crawler.crawl()
    print(f"\n✅ Crawled {len(results)} pages")
    for r in results:
        print(f"  - {r['url']}: {len(r['content'])} chars")

asyncio.run(test())
