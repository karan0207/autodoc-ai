import pytest
import asyncio
import os
from backend.crawler.crawler import Crawler
from backend.processors.chunker import Chunker
from backend.embeddings.embedder import Embedder
from backend.embeddings.vector_store import VectorStore
from backend.rag.generator import Generator

# 1. Test Crawler
@pytest.mark.asyncio
async def test_crawler():
    print("\n🕷️ Testing Crawler...")
    url = "https://example.com"
    crawler = Crawler(url)
    results = await crawler.crawl()
    
    assert len(results) > 0
    assert "Example Domain" in results[0]['content']
    print("✅ Crawler working! Fetched content.")

# 2. Test Chunker
def test_chunker():
    print("\n🔪 Testing Chunker...")
    text = "This is a test sentence. " * 50
    chunker = Chunker()
    chunks = chunker.chunk_text(text, {"url": "test", "source": "test"})
    
    assert len(chunks) > 0
    assert len(chunks[0]['content']) <= 1000
    print(f"✅ Chunker working! Created {len(chunks)} chunks.")

# 3. Test Embedder
@pytest.mark.asyncio
async def test_embedder():
    print("\n🧠 Testing Embedder...")
    embedder = Embedder()
    texts = ["Hello world", "This is a test"]
    embeddings = await embedder.embed_texts(texts)
    
    assert len(embeddings) == 2
    assert len(embeddings[0]) == 384  # Check dimension
    print("✅ Embedder working! Generated vectors.")

# 4. Test Vector Store
def test_vector_store():
    print("\n💾 Testing Vector Store...")
    store = VectorStore()
    
    # Create a dummy chunk with vector
    chunk = {
        "content": "Test content for vector store",
        "url": "test-url",
        "source": "test",
        "job_id": "test-job-123",
        "vector": [0.1] * 384
    }
    
    # Add
    store.add_chunks([chunk])
    
    # Search
    results = store.search_by_vector([0.1] * 384, limit=1)
    
    assert len(results) > 0
    assert results[0].properties['content'] == "Test content for vector store"
    print("✅ Vector Store working! Stored and retrieved.")

# 5. Test Generator (LLM)
@pytest.mark.asyncio
async def test_generator():
    print("\n🤖 Testing Generator (LLM)...")
    generator = Generator()
    
    context = [
        {"url": "test", "content": "AutoDoc AI is a tool that generates documentation automatically."}
    ]
    
    response = await generator.generate("What is AutoDoc AI?", context)
    
    assert len(response) > 0
    assert "AutoDoc AI" in response
    print(f"✅ Generator working! Response: {response[:50]}...")
