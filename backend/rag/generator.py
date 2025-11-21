import httpx
import os
from typing import List, Dict
import logging
import json

logger = logging.getLogger(__name__)

class Generator:
    def __init__(self):
        self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.model = "llama3.2:1b"  # Faster 1B parameter model
        logger.info(f"Using Ollama at {self.ollama_url} with model {self.model}")

    async def generate(self, prompt: str, context: List[Dict]) -> str:
        # Construct context string
        context_str = "\n\n".join([f"Source: {c['url']}\nContent: {c['content']}" for c in context])
        
        system_prompt = """You are an expert technical writer. 
        Use the provided context to answer the user's request or generate documentation.
        If the answer is not in the context, say so.
        Always cite your sources if possible."""

        user_prompt = f"""Context:
        {context_str}
        
        Request:
        {prompt}
        """

        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": f"{system_prompt}\n\n{user_prompt}",
                        "stream": False
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("response", "No response generated")
                else:
                    error_msg = f"Ollama returned status {response.status_code}"
                    logger.error(error_msg)
                    return f"Error: {error_msg}. Make sure Ollama is running and the model '{self.model}' is pulled.\nRun: docker exec -it crawler-ollama-1 ollama pull {self.model}"
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            return f"Error generating content: {e}\n\nMake sure Ollama is running: docker-compose up -d"
