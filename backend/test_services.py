"""
Test script to verify backend services one by one.

Run this to check if each service is configured correctly.
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

print("=" * 60)
print("Backend Services Test")
print("=" * 60)

# Test 1: Check .env file
print("\n1. Testing .env file loading...")
from dotenv import load_dotenv
load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
jina_key = os.getenv("JINA_API_KEY")
groq_key = os.getenv("GROQ_API_KEY")

print(f"   SUPABASE_URL: {'✓ Set' if supabase_url else '✗ Missing'}")
print(f"   SUPABASE_SERVICE_KEY: {'✓ Set (' + supabase_key[:20] + '...)' if supabase_key else '✗ Missing'}")
print(f"   JINA_API_KEY: {'✓ Set' if jina_key else '✗ Missing'}")
print(f"   GROQ_API_KEY: {'✓ Set' if groq_key else '✗ Missing'}")

if not all([supabase_url, supabase_key, jina_key, groq_key]):
    print("\n❌ Missing required environment variables!")
    print("   Check that backend/.env file exists and is properly formatted")
    sys.exit(1)

# Test 2: Supabase Connection
print("\n2. Testing Supabase connection...")
try:
    from backend.services.supabase_client import SupabaseClient
    client = SupabaseClient.get_client()
    
    # Try a simple query
    result = client.table("chunks").select("count", count="exact").limit(0).execute()
    print(f"   ✓ Supabase connected successfully")
    print(f"   Database has {result.count if hasattr(result, 'count') else 0} chunks")
except Exception as e:
    print(f"   ✗ Supabase connection failed: {e}")
    print("   Make sure you've run the SQL migration in Supabase dashboard")

# Test 3: Jina Scraper
print("\n3. Testing Jina Scraper...")
try:
    from backend.services.jina_scraper import JinaScraper
    scraper = JinaScraper()
    print(f"   ✓ Jina Scraper initialized")
except Exception as e:
    print(f"   ✗ Jina Scraper failed: {e}")

# Test 4: Jina Embedder
print("\n4. Testing Jina Embedder...")
try:
    from backend.services.jina_embedder import JinaEmbedder
    embedder = JinaEmbedder()
    print(f"   ✓ Jina Embedder initialized (768-dim)")
except Exception as e:
    print(f"   ✗ Jina Embedder failed: {e}")

# Test 5: Groq Client
print("\n5. Testing Groq Client...")
try:
    from backend.services.groq_client import GroqClient
    groq = GroqClient()
    print(f"   ✓ Groq Client initialized")
except Exception as e:
    print(f"   ✗ Groq Client failed: {e}")

# Test 6: Vector Store
print("\n6. Testing Vector Store...")
try:
    from backend.embeddings.vector_store import VectorStore
    store = VectorStore()
    stats = store.get_stats()
    print(f"   ✓ Vector Store initialized")
    print(f"   Total chunks: {stats.get('total_chunks', 0)}")
except Exception as e:
    print(f"   ✗ Vector Store failed: {e}")

print("\n" + "=" * 60)
print("Test Complete!")
print("=" * 60)
