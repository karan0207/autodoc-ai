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
        # SIMPLIFIED INGESTION FOR PROTOTYPE
        logger.info(f"🚀 Starting simplified ingestion for job {job_id}")
        
        # Initialize vector store (Singleton)
        vector_store = VectorStore()
        
        # 1. Crawl Website (Simulated/Lightweight)
        logger.info(f"🕷️ Crawling {req.url}...")
        web_content = f"Content from {req.url}. This is a simulated crawl for prototype speed."
        
        # 2. Fetch GitHub (Simulated/Lightweight)
        logger.info(f"🔍 Fetching from {req.repo_url}...")
        repo_content = f"README content from {req.repo_url}. AutoDoc AI is a tool for generating documentation."
        
        # 3. Create Chunks (Directly)
        all_chunks = [
            {
                "content": web_content,
                "metadata": {"url": req.url, "source": "website", "job_id": job_id},
                "vector": [0.1] * 384 # Mock vector
            },
            {
                "content": repo_content,
                "metadata": {"url": req.repo_url, "source": "github", "job_id": job_id},
                "vector": [0.1] * 384 # Mock vector
            }
        ]
        
        # 4. Store in Simple Vector Store
        logger.info(f"💾 Storing {len(all_chunks)} chunks in vector store...")
        vector_store.add_chunks(all_chunks)
        
        # Don't close the singleton store!
        # vector_store.close()
        
        logger.info(f"🎉 Job {job_id} completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Ingestion failed for job {job_id}: {e}", exc_info=True)
        raise

@router.post("/ingest")
async def start_ingest(req: IngestRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    
    # Run synchronously for debugging/prototype to ensure it completes
    await process_ingestion(job_id, req)
    
    # background_tasks.add_task(process_ingestion, job_id, req)
    
    return {"status": "processing", "job_id": job_id}
