import asyncio
from services.local_embedder import LocalEmbedder

async def test():
    print("Testing Local Embeddings...")
    
    embedder = LocalEmbedder()
    
    texts = ["Hello world", "This is a test"]
    embeddings = await embedder.embed(texts)
    
    print(f"✅ Generated {len(embeddings)} embeddings")
    print(f"✅ Dimensions: {len(embeddings[0])}")
    print(f"✅ Sample: {embeddings[0][:3]}")

asyncio.run(test())
