import os
from dotenv import load_dotenv

load_dotenv()

print("Testing Supabase...")
try:
    from supabase import create_client
    
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_SERVICE_KEY')
    
    print(f"URL: {url}")
    print(f"Key: {key[:30]}...")
    
    client = create_client(url, key)
    result = client.table('chunks').select('count', count='exact').limit(0).execute()
    
    print(f"✅ Supabase connection successful!")
    print(f"Chunks in database: {result.count if hasattr(result, 'count') else 0}")
    
except Exception as e:
    print(f"❌ Supabase test failed: {e}")
    import traceback
    traceback.print_exc()
