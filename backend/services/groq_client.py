"""
Groq API client for ultra-fast LLM inference.

Provides 500+ tokens/second generation speed.
"""

from groq import AsyncGroq
from typing import Optional, List, Dict
import logging
import os
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class GroqClient:
    """LLM client using Groq API for fast inference."""
    
    DEFAULT_MODEL = "llama-3.1-70b-versatile"  # Fast and high quality
    
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY must be set in .env")
        
        self.client = AsyncGroq(api_key=self.api_key)
    
    async def generate(
        self,
        prompt: str,
        context: Optional[List[Dict]] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> str:
        """
        Generate text using Groq API.
        
        Args:
            prompt: The instruction/question
            context: Optional list of context chunks
            model: Model name (default: llama-3.1-70b-versatile)
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text content
        """
        try:
            # Build system message with context
            system_content = "You are an expert technical documentation writer."
            
            if context:
                context_text = "\n\n".join([
                    f"Source {i+1}:\n{chunk.get('content', '')}"
                    for i, chunk in enumerate(context[:5])  # Limit to top 5
                ])
                system_content += f"\n\nUse the following context to answer:\n\n{context_text}"
            
            messages = [
                {"role": "system", "content": system_content},
                {"role": "user", "content": prompt}
            ]
            
            logger.info(f"🚀 Generating with Groq ({model or self.DEFAULT_MODEL})...")
            
            response = await self.client.chat.completions.create(
                model=model or self.DEFAULT_MODEL,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            content = response.choices[0].message.content
            
            logger.info(f"✅ Generated {len(content)} characters")
            return content
            
        except Exception as e:
            logger.error(f"❌ Generation failed: {e}")
            raise
    
    async def generate_stream(
        self,
        prompt: str,
        context: Optional[List[Dict]] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ):
        """
        Generate text with streaming for real-time output.
        
        Yields chunks of text as they are generated.
        """
        try:
            # Build system message with context
            system_content = "You are an expert technical documentation writer."
            
            if context:
                context_text = "\n\n".join([
                    f"Source {i+1}:\n{chunk.get('content', '')}"
                    for i, chunk in enumerate(context[:5])
                ])
                system_content += f"\n\nUse the following context to answer:\n\n{context_text}"
            
            messages = [
                {"role": "system", "content": system_content},
                {"role": "user", "content": prompt}
            ]
            
            logger.info(f"🚀 Streaming generation with Groq...")
            
            stream = await self.client.chat.completions.create(
                model=model or self.DEFAULT_MODEL,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
            
            logger.info(f"✅ Streaming complete")
            
        except Exception as e:
            logger.error(f"❌ Streaming failed: {e}")
            raise
