from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from ..crawler.crawler import Crawler
from ..github.fetcher import GitHubFetcher
from ..processors.chunker import Chunker
from ..embeddings.vector_store import VectorStore
from ..embeddings.embedder import Embedder
import uuid
import logging
import asyncio

router = APIRouter()
logger = logging.getLogger(__name__)

class IngestRequest(BaseModel):
    url: str
    repo_url: str

async def process_ingestion(job_id: str, req: IngestRequest):
    logger.info(f"Starting ingestion for job {job_id}")
    print(f"🚀 Starting ingestion for job {job_id}")  # DEBUG
    
    try:
        # 1. Crawl Website
        logger.info(f"Crawling {req.url}...")
        print(f"🕷️ Crawling {req.url}...")  # DEBUG
        crawler = Crawler(req.url)
        web_results = await crawler.crawl()
        logger.info(f"Crawled {len(web_results)} pages")
        print(f"✅ Crawled {len(web_results)} pages")  # DEBUG
        
        if not web_results:
            logger.warning("No pages were crawled. Check the URL and crawler logs.")
            print(f"⚠️  No pages were crawled")  # DEBUG
        
        # 2. Fetch GitHub
        logger.info(f"Fetching from {req.repo_url}...")
        gh_fetcher = GitHubFetcher(req.repo_url)
        
        # Fetch README
        readme = await gh_fetcher.fetch_file("README.md")
        
        # Fetch Changelog
        changelog = await gh_fetcher.fetch_file("CHANGELOG.md")
        
        logger.info(f"Fetched GitHub data. README: {'Yes' if readme else 'No'}, Changelog: {'Yes' if changelog else 'No'}")
        
        # Initialize components
        chunker = Chunker()
        vector_store = VectorStore()
        embedder = Embedder()
        
        all_chunks = []
        
        # Process Web Results
        for page in web_results:
            chunks = chunker.chunk_text(page['content'], {
                "url": page['url'],
                "source": "website",
                "job_id": job_id
            })
            all_chunks.extend(chunks)
            
        # Process GitHub Results
        if readme:
            chunks = chunker.chunk_text(readme, {
                "url": req.repo_url + "/blob/main/README.md",
                "source": "github",
                "job_id": job_id
            })
            all_chunks.extend(chunks)
            
        if changelog:
            chunks = chunker.chunk_text(changelog, {
                "url": req.repo_url + "/blob/main/CHANGELOG.md",
                "source": "github",
                "job_id": job_id
            })
            all_chunks.extend(chunks)

        # Fetch Commits
        commits = await gh_fetcher.fetch_commits(limit=10)
        if commits:
            commit_text = "\n".join([f"Commit: {c['commit']['message']} (Date: {c['commit']['author']['date']})" for c in commits])
            chunks = chunker.chunk_text(commit_text, {
                "url": req.repo_url + "/commits",
                "source": "github-commits",
                "job_id": job_id
            })
            all_chunks.extend(chunks)
            
        # Store in Vector DB
        if all_chunks:
            # Generate embeddings in batches
            texts = [c["content"] for c in all_chunks]
            batch_size = 50
            
            for i in range(0, len(texts), batch_size):
                batch_texts = texts[i:i+batch_size]
                batch_chunks = all_chunks[i:i+batch_size]
                
                try:
                    embeddings = await embedder.embed_texts(batch_texts)
                    for chunk, vector in zip(batch_chunks, embeddings):
                        chunk["vector"] = vector
                        
                    # Run blocking Weaviate operation in threadpool
                    await asyncio.get_running_loop().run_in_executor(
                        None, vector_store.add_chunks, batch_chunks
                    )
                except Exception as e:
                    logger.error(f"Failed to process batch {i}: {e}")
            
        vector_store.close()
        
        logger.info(f"Job {job_id} completed. Stored {len(all_chunks)} chunks.")
        print(f"🎉 Job {job_id} completed. Stored {len(all_chunks)} chunks.")  # DEBUG
        
    except Exception as e:
        logger.error(f"Ingestion failed for job {job_id}: {e}", exc_info=True)
        print(f"❌ Ingestion failed for job {job_id}: {e}")  # DEBUG
        raise  # Re-raise to see the full traceback

@router.post("/ingest")
async def start_ingest(req: IngestRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    background_tasks.add_task(process_ingestion, job_id, req)
    return {"job_id": job_id, "status": "started"}
