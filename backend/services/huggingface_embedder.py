"""
HuggingFace embeddings service using Inference API.

Provides free embeddings via HuggingFace's serverless inference.
"""

import httpx
from typing import List, Union
import logging
import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env from backend directory
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

logger = logging.getLogger(__name__)


class HuggingFaceEmbedder:
    """Embeddings generator using HuggingFace Inference API."""
    
    # Use the model hub API endpoint
    MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"
    API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
    
    def __init__(self):
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        if not self.api_key:
            raise ValueError("HUGGINGFACE_API_KEY must be set in .env")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
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
            List of embedding vectors (384-dimensional)
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
        
        logger.info(f"✅ Generated {len(all_embeddings)} embeddings via HuggingFace")
        return all_embeddings
    
    async def _embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Embed a single batch of texts."""
        try:
            async with httpx.AsyncClient(timeout=60) as client:
                payload = {
                    "inputs": texts,
                    "options": {"wait_for_model": True}
                }
                
                logger.info(f"🔮 Generating embeddings for {len(texts)} texts via HuggingFace...")
                response = await client.post(
                    self.API_URL,
                    headers=self.headers,
                    json=payload
                )
                response.raise_for_status()
                
                # HuggingFace returns embeddings directly as a list
                embeddings = response.json()
                
                # Handle single text case (returns single embedding)
                if isinstance(embeddings, list) and len(embeddings) > 0:
                    if isinstance(embeddings[0], (int, float)):
                        # Single embedding returned as flat list
                        return [embeddings]
                    else:
                        # Multiple embeddings
                        return embeddings
                
                return embeddings
                
        except httpx.HTTPError as e:
            logger.error(f"❌ HuggingFace embedding failed: {e}")
            raise
    
    def get_dimensions(self) -> int:
        """Get embedding vector dimensions."""
        return 384  # all-MiniLM-L6-v2 is 384-dimensional
