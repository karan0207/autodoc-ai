import logging
import time
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

print("🧪 Testing Sentence Transformer Loading & Inference...")

try:
    print("1. Importing sentence_transformers...")
    start_import = time.time()
    from sentence_transformers import SentenceTransformer
    print(f"   ✅ Import took {time.time() - start_import:.2f}s")

    print("2. Loading model 'all-MiniLM-L6-v2'...")
    start_load = time.time()
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print(f"   ✅ Model load took {time.time() - start_load:.2f}s")

    print("3. Running inference on sample text...")
    start_infer = time.time()
    text = "This is a test sentence to check embedding generation speed."
    embedding = model.encode(text)
    print(f"   ✅ Inference took {time.time() - start_infer:.2f}s")
    print(f"   ✅ Embedding shape: {embedding.shape}")

    print("\n🎉 SUCCESS: Embedding model is working correctly!")

except Exception as e:
    print(f"\n❌ FAILED: {e}")
    import traceback
    traceback.print_exc()
