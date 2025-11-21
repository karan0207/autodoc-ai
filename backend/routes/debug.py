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
        vector_store = VectorStore()
        
        # Get collection
        collection = vector_store.client.collections.get(vector_store.collection_name)
        
        # Run aggregate in thread pool
        aggregate = await asyncio.get_running_loop().run_in_executor(
            None,
            lambda: collection.aggregate.over_all(total_count=True)
        )
        
        total_count = aggregate.total_count
        
        # Get some sample objects
        if job_id:
            # Filter by job_id
            import weaviate.classes.query as wvc_query
            response = await asyncio.get_running_loop().run_in_executor(
                None,
                lambda: collection.query.fetch_objects(
                    limit=5,
                    filters=wvc_query.Filter.by_property("job_id").equal(job_id)
                )
            )
        else:
            # Get all
            response = await asyncio.get_running_loop().run_in_executor(
                None,
                lambda: collection.query.fetch_objects(limit=5)
            )
        
        samples = [
            {
                "job_id": obj.properties.get("job_id"),
                "source": obj.properties.get("source"),
                "url": obj.properties.get("url"),
                "content_preview": obj.properties.get("content", "")[:100]
            }
            for obj in response.objects
        ]
        
        vector_store.close()
        
        return {
            "total_documents": total_count,
            "samples": samples,
            "filtered_by_job_id": job_id
        }
    except Exception as e:
        logger.error(f"Debug stats failed: {e}")
        return {"error": str(e)}
