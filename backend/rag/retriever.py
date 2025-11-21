from ..embeddings.vector_store import VectorStore
from ..embeddings.embedder import Embedder
from typing import List, Dict
import logging
import asyncio

logger = logging.getLogger(__name__)

class Retriever:
    def __init__(self):
        self.vector_store = VectorStore()
        self.embedder = Embedder()

    async def retrieve(self, query: str, job_id: str = None, limit: int = 5) -> List[Dict]:
        # 1. Embed query
        # Note: Weaviate v4 with 'none' vectorizer expects us to handle embeddings or use a module.
        # Since we are manually embedding chunks, we might need to embed the query too if we were using vector search directly.
        # However, the current VectorStore.search implementation uses `near_text` which usually relies on Weaviate's internal vectorizer if configured,
        # OR we need to pass the vector.
        
        # Let's check VectorStore.search implementation again.
        # It uses `near_text`. If we didn't configure a vectorizer in docker-compose (we set DEFAULT_VECTORIZER_MODULE: 'none'),
        # `near_text` might fail without a module.
        # We should probably use `near_vector` instead.
        
        logger.info(f"Creating embedding for query: {query[:50]}...")
        query_embedding = (await self.embedder.embed_texts([query]))[0]
        
        logger.info(f"Searching vector store with job_id={job_id}, limit={limit}")
        # Run blocking Weaviate search in threadpool
        results = await asyncio.get_running_loop().run_in_executor(
            None, 
            lambda: self.vector_store.search_by_vector(query_embedding, limit, job_id)
        )
        
        logger.info(f"Found {len(results)} results from vector store")
        
        # Close the connection
        self.vector_store.close()
        
        return [
            {
                "content": r.properties["content"],
                "url": r.properties["url"],
                "source": r.properties["source"]
            }
            for r in results
        ]
