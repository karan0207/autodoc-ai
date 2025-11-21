import httpx

async def test_weaviate():
    """Test if data is in Weaviate"""
    async with httpx.AsyncClient() as client:
        # Check if collection exists
        response = await client.get("http://localhost:8080/v1/schema/Document")
        print("Schema:", response.json())
        
        # Try to query all objects
        response = await client.get("http://localhost:8080/v1/objects?class=Document&limit=10")
        print("\nObjects:", response.json())

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_weaviate())
