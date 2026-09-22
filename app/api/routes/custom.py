from fastapi import APIRouter, Depends
from app.api.deps import async_http_client, sync_http_client


router = APIRouter(tags=["custom"])

@router.get("/test_async")
async def test_async(client= Depends(async_http_client)):
    response = await client.get("https://jsonplaceholder.typicode.com/todos")
    return response.json()

@router.get("/test_sync")
def test_sync(client= Depends(sync_http_client)):
    response = client.get("https://jsonplaceholder.typicode.com/todos")
    return response.json()