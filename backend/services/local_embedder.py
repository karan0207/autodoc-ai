"""
Local embeddings using sentence-transformers.

Completely free and reliable - no API needed.
"""

from typing import List, Union
import logging
import asyncio

logger = logging.getLogger(__name__)


class LocalEmbedder:
    """Local embeddings generator using sentence-transformers."""
    
    MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
    
    def __init__(self):
        logger.info("🔄 Loading local sentence-transformers model...")
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(self.MODEL_NAME, device='cpu')
            logger.info("✅ Local embedder ready (384 dimensions)")
        except ImportError:
            raise ImportError("sentence-transformers not installed. Run: pip install sentence-transformers")
        except Exception as e:
            logger.error(f"❌ Failed to load model: {e}")
            raise
    
    async def embed(
        self, 
        texts: Union[str, List[str]], 
        batch_size: int = 32
    ) -> List[List[float]]:
        """
        Generate embeddings for one or more texts.
        
        Args:
            texts: Single text string or list of texts
            batch_size: Not used for local (can process all at once)
            
        Returns:
            List of embedding vectors (384-dimensional)
        """
        if isinstance(texts, str):
            texts = [texts]
        
        logger.info(f"🔮 Generating embeddings for {len(texts)} texts locally...")
        
        try:
            # Run in thread pool to avoid blocking async loop
            loop = asyncio.get_event_loop()
            embeddings = await loop.run_in_executor(
                None,
                lambda: self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False).tolist()
            )
            
            logger.info(f"✅ Generated {len(embeddings)} embeddings")
            return embeddings
            
        except Exception as e:
            logger.error(f"❌ Local embedding failed: {e}")
            raise
    
    def get_dimensions(self) -> int:
        """Get embedding vector dimensions."""
        return 384
