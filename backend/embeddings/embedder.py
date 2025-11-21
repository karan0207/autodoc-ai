import os
from typing import List
import logging

logger = logging.getLogger(__name__)

class Embedder:
    def __init__(self):
        # Use sentence-transformers for local embeddings
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self.local = True
            logger.info("Using local sentence-transformers for embeddings")
        except ImportError:
            logger.warning("sentence-transformers not installed. Using mock embeddings.")
            self.model = None
            self.local = False

    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
            
        if not self.model:
            # Return mock embeddings (384 dimensions for all-MiniLM-L6-v2 compatibility)
            return [[0.0] * 384 for _ in texts]
            
        try:
            # Run blocking operation in threadpool
            import asyncio
            loop = asyncio.get_event_loop()
            embeddings = await loop.run_in_executor(None, self.model.encode, texts)
            return [emb.tolist() for emb in embeddings]
        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            return [[0.0] * 384 for _ in texts]
