"""Quick API test to verify embeddings are working"""
import httpx
import asyncio

async def test_api():
    print("Testing backend API...")
    
    # Test health endpoint
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://127.0.0.1:8000/api/health")
            print(f"✅ Health check: {response.status_code}")
            if response.status_code == 200:
                print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # Test settings endpoint to check embeddings status
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://127.0.0.1:8000/api/settings")
            print(f"✅ Settings check: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Embeddings ready: {data.get('embeddings_ready', 'unknown')}")
                print(f"   Embeddings model: {data.get('embedding_model', 'unknown')}")
                if not data.get('embeddings_ready'):
                    print(f"   ⚠️  Embeddings not ready! Check server logs.")
    except Exception as e:
        print(f"❌ Settings check failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_api())
