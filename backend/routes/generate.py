from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..rag.retriever import Retriever
from ..rag.generator import Generator
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class GenerateRequest(BaseModel):
    job_id: str
    prompt: str
    type: str = "custom" # api, product, changelog, custom

@router.post("/generate")
async def generate_docs(req: GenerateRequest):
    try:
        retriever = Retriever()
        generator = Generator()
        
        # 1. Retrieve context
        logger.info(f"Retrieving context for job {req.job_id} with prompt: {req.prompt}")
        context = await retriever.retrieve(req.prompt, job_id=req.job_id)
        
        logger.info(f"Retrieved {len(context)} context chunks for job {req.job_id}")
        
        if not context:
            logger.warning(f"No context found for job_id: {req.job_id}. Check if ingestion completed successfully.")
            return {"content": "No relevant context found to generate documentation.", "sources": []}
            
        # 2. Generate content
        # Adjust prompt based on type
        final_prompt = req.prompt
        if req.type == "api":
            final_prompt = f"Generate a detailed API Reference based on the following context. {req.prompt}"
        elif req.type == "product":
            final_prompt = f"Write a comprehensive Product Description. {req.prompt}"
        elif req.type == "changelog":
            final_prompt = f"Summarize the recent changes and changelog. {req.prompt}"
            
        content = await generator.generate(final_prompt, context)
        
        return {
            "content": content,
            "sources": context
        }
        
    except Exception as e:
        logger.error(f"Generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
