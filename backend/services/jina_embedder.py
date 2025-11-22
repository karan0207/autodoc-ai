"""
Jina AI embeddings service for generating vector embeddings.

Provides fast, API-based embeddings without local model loading.
"""

import httpx
from typing import List, Union
import logging
import os
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class JinaEmbedder:
    """Embeddings generator using Jina AI Embeddings API."""
    
    API_URL = "https://api.jina.ai/v1/embeddings"
    MODEL = "jina-embeddings-v2-base-en"  # 768 dimensions
    
    def __init__(self):
        self.api_key = os.getenv("JINA_API_KEY")
        if not self.api_key:
            raise ValueError("JINA_API_KEY must be set in .env")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def embed(
        self, 
        texts: Union[str, List[str]], 
        batch_size: int = 32
    ) -> List[List[float]]:
        """
        Generate embeddings for one or more texts.
        
        Args:
            texts: Single text string or list of texts
            batch_size: Maximum texts per API call
            
        Returns:
            List of embedding vectors (768-dimensional)
        """
        # Normalize input to list
        if isinstance(texts, str):
            texts = [texts]
        
        all_embeddings = []
        
        # Process in batches
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            embeddings = await self._embed_batch(batch)
            all_embeddings.extend(embeddings)
        
        logger.info(f"✅ Generated {len(all_embeddings)} embeddings")
        return all_embeddings
    
    async def _embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Embed a single batch of texts."""
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                payload = {
                    "model": self.MODEL,
                    "input": texts
                }
                
                logger.info(f"🔮 Generating embeddings for {len(texts)} texts...")
                response = await client.post(
                    self.API_URL,
                    headers=self.headers,
                    json=payload
                )
                response.raise_for_status()
                
                data = response.json()
                embeddings = [item["embedding"] for item in data["data"]]
                
                return embeddings
                
        except httpx.HTTPError as e:
            logger.error(f"❌ Embedding generation failed: {e}")
            raise
    
    def get_dimensions(self) -> int:
        """Get embedding vector dimensions."""
        return 768
