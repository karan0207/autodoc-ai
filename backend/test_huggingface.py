import os
import asyncio
from dotenv import load_dotenv
from pathlib import Path

# Load env
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

async def test():
    print("Testing HuggingFace Embeddings...")
    print(f"API Key: {os.getenv('HUGGINGFACE_API_KEY')[:20]}...")
    
    from services.huggingface_embedder import HuggingFaceEmbedder
    
    embedder = HuggingFaceEmbedder()
    
    # Test with a simple text
    texts = ["Hello world", "This is a test"]
    embeddings = await embedder.embed(texts)
    
    print(f"✅ Generated {len(embeddings)} embeddings")
    print(f"✅ Dimension: {len(embeddings[0])}")
    print(f"✅ First embedding preview: {embeddings[0][:5]}")

asyncio.run(test())
