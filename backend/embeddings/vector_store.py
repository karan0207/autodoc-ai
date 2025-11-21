import weaviate
import weaviate.classes.config as wvc
import weaviate.classes.query as wvc_query
import os
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self):
        # Connect to local Weaviate
        self.client = weaviate.connect_to_local(
            host="localhost",
            port=8080,
            grpc_port=50051
        )
        self.collection_name = "Document"
        self._init_schema()

    def _init_schema(self):
        try:
            if not self.client.collections.exists(self.collection_name):
                self.client.collections.create(
                    name=self.collection_name,
                    properties=[
                        wvc.Property(name="content", data_type=wvc.DataType.TEXT),
                        wvc.Property(name="url", data_type=wvc.DataType.TEXT),
                        wvc.Property(name="source", data_type=wvc.DataType.TEXT),
                        wvc.Property(name="job_id", data_type=wvc.DataType.TEXT),
                    ]
                )
                logger.info(f"Created collection {self.collection_name}")
        except Exception as e:
            logger.error(f"Failed to init schema: {e}")

    def add_chunks(self, chunks: List[Dict]):
        collection = self.client.collections.get(self.collection_name)
        try:
            with collection.batch.dynamic() as batch:
                for chunk in chunks:
                    batch.add_object(
                        properties={
                            "content": chunk["content"],
                            "url": chunk["metadata"].get("url", ""),
                            "source": chunk["metadata"].get("source", "unknown"),
                            "job_id": chunk["metadata"].get("job_id", ""),
                        },
                        vector=chunk.get("vector")
                    )
            logger.info(f"Added {len(chunks)} chunks to Weaviate")
        except Exception as e:
            logger.error(f"Failed to add chunks: {e}")

    def search(self, query: str, limit: int = 5, job_id: str = None):
        collection = self.client.collections.get(self.collection_name)
        
        filters = None
        if job_id:
            filters = wvc_query.Filter.by_property("job_id").equal(job_id)
            
        response = collection.query.near_text(
            query=query,
            limit=limit,
            filters=filters
        )
        return response.objects

    def search_by_vector(self, vector: List[float], limit: int = 5, job_id: str = None):
        collection = self.client.collections.get(self.collection_name)
        
        filters = None
        if job_id:
            filters = wvc_query.Filter.by_property("job_id").equal(job_id)
            
        response = collection.query.near_vector(
            near_vector=vector,
            limit=limit,
            filters=filters
        )
        return response.objects

    def close(self):
        self.client.close()
