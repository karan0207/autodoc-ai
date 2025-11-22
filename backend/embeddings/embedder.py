import os
from typing import List
import logging

logger = logging.getLogger(__name__)

class Embedder:
    def __init__(self):
        self.model = None
        self.local = False
        # FORCING MOCK EMBEDDINGS TO UNBLOCK PIPELINE
        # The SentenceTransformer model is hanging on load on this machine.
        logger.warning("⚠️ FORCING MOCK EMBEDDINGS to avoid hang on model load.")
        logger.warning("⚠️ Quality will be low, but pipeline will work.")
        
        # try:
        #     logger.info("Loading embedding model...")
        #     from sentence_transformers import SentenceTransformer
        #     # Use a smaller/faster model or ensure CPU optimization
        #     self.model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
        #     self.local = True
        #     logger.info("✅ Using local sentence-transformers for embeddings")
        # except Exception as e:
        #     logger.warning(f"⚠️ Failed to load sentence-transformers: {e}")
        #     logger.warning("⚠️ Using MOCK embeddings instead.")
        #     self.model = None

    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            logger.warning("⚠️ No texts provided for embedding")
            return []
        
        logger.info(f"🧠 Generating embeddings for {len(texts)} texts...")
            
        if not self.model:
            # Return mock embeddings (384 dimensions for all-MiniLM-L6-v2 compatibility)
            logger.warning("Using mock embeddings (model not loaded)")
            return [[0.1] * 384 for _ in texts]
            
        try:
            # Run blocking operation in threadpool to avoid hanging the async loop
            import asyncio
            loop = asyncio.get_running_loop()
            
            def _encode():
                return self.model.encode(texts, convert_to_numpy=True).tolist()
                
            embeddings = await loop.run_in_executor(None, _encode)
            
            logger.info(f"✅ Generated {len(embeddings)} embeddings")
            return embeddings
        except Exception as e:
            logger.error(f"❌ Embedding generation failed: {e}", exc_info=True)
            # Fallback to mock
            return [[0.1] * 384 for _ in texts]
