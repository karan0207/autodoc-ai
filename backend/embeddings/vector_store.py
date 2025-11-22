import os
from typing import List, Dict
import logging
import json

logger = logging.getLogger(__name__)

class VectorStore:
    """Simple in-memory vector store for prototyping (Singleton)"""
    _instance = None
    _chunks = []  # Class-level storage
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VectorStore, cls).__new__(cls)
            logger.info("📦 Initializing simple in-memory vector store (Singleton)...")
        return cls._instance

    def __init__(self):
        # Don't reset chunks on re-init
        pass
        
    @property
    def chunks(self):
        return VectorStore._chunks
        
    def add_chunks(self, chunks: List[Dict]):
        """Add chunks to the store"""
        logger.info(f"📝 Adding {len(chunks)} chunks to vector store...")
        
        try:
            for idx, chunk in enumerate(chunks):
                # Store the chunk with all its data
                stored_chunk = {
                    "content": chunk["content"],
                    "url": chunk["metadata"].get("url", ""),
                    "source": chunk["metadata"].get("source", "unknown"),
                    "job_id": chunk["metadata"].get("job_id", ""),
                    "vector": chunk.get("vector", [])
                }
                VectorStore._chunks.append(stored_chunk)
                
                if (idx + 1) % 10 == 0:
                    logger.info(f"  Stored {idx + 1}/{len(chunks)} chunks...")
            
            logger.info(f"✅ Successfully added {len(chunks)} chunks (total: {len(VectorStore._chunks)})")
        except Exception as e:
            logger.error(f"❌ Failed to add chunks: {e}", exc_info=True)
            raise
    
    def search_by_vector(self, vector: List[float], limit: int = 5, job_id: str = None):
        """Search for similar vectors using cosine similarity"""
        logger.info(f"� Searching for {limit} similar chunks (job_id: {job_id})...")
        
        try:
            # Filter by job_id if provided
            filtered_chunks = self.chunks
            if job_id:
                filtered_chunks = [c for c in self.chunks if c["job_id"] == job_id]
                logger.info(f"  Filtered to {len(filtered_chunks)} chunks for job_id: {job_id}")
            
            if not filtered_chunks:
                logger.warning(f"⚠️ No chunks found for job_id: {job_id}")
                return []
            
            # Calculate cosine similarity
            import numpy as np
            
            results = []
            query_vec = np.array(vector)
            
            for chunk in filtered_chunks:
                if not chunk["vector"]:
                    continue
                    
                chunk_vec = np.array(chunk["vector"])
                
                # Cosine similarity
                similarity = np.dot(query_vec, chunk_vec) / (
                    np.linalg.norm(query_vec) * np.linalg.norm(chunk_vec)
                )
                
                results.append({
                    "similarity": float(similarity),
                    "chunk": chunk
                })
            
            # Sort by similarity (highest first)
            results.sort(key=lambda x: x["similarity"], reverse=True)
            
            # Return top results as mock Weaviate objects
            top_results = results[:limit]
            logger.info(f"✅ Found {len(top_results)} results")
            
            # Create mock objects that match Weaviate's API
            class MockObject:
                def __init__(self, properties):
                    self.properties = properties
            
            return [MockObject(r["chunk"]) for r in top_results]
            
        except Exception as e:
            logger.error(f"❌ Search failed: {e}", exc_info=True)
            return []
    
    def search(self, query: str, limit: int = 5, job_id: str = None):
        """Search using text query (not implemented for simple store)"""
        logger.warning("⚠️ Text search not supported in simple store, use search_by_vector")
        return []
    
    def close(self):
        """Close the connection (no-op for in-memory store)"""
        logger.info(f"📊 Vector store stats: {len(self.chunks)} total chunks stored")
        pass
