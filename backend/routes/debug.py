from fastapi import APIRouter
from ..embeddings.vector_store import VectorStore
import logging
import asyncio

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/debug/stats")
async def get_stats(job_id: str = None):
    """Get statistics about what's stored in the vector database"""
    try:
        logger.info("🔍 Debug stats request started...")
        vector_store = VectorStore()
        logger.info("✅ Connected to vector store")
        
        # Get total count
        total_count = len(vector_store.chunks)
        logger.info(f"Total chunks in store: {total_count}")
        
        # Filter samples by job_id if provided
        if job_id:
            samples_data = [c for c in vector_store.chunks if c.get("job_id") == job_id][:5]
            logger.info(f"Found {len(samples_data)} samples for job_id: {job_id}")
        else:
            samples_data = vector_store.chunks[:5]
        
        samples = [
            {
                "job_id": chunk.get("job_id"),
                "source": chunk.get("source"),
                "url": chunk.get("url"),
                "content_preview": chunk.get("content", "")[:100]
            }
            for chunk in samples_data
        ]
        
        vector_store.close()
        logger.info("✅ Debug stats completed successfully")
        
        return {
            "total_documents": total_count,
            "samples": samples,
            "filtered_by_job_id": job_id
        }
    except Exception as e:
        logger.error(f"❌ Debug stats failed: {e}", exc_info=True)
        return {"error": str(e), "total_documents": 0, "samples": []}
