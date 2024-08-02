import pytest
import httpx

@pytest.mark.asyncio
async def test_unauthorized_access():
    # Define the URL and invalid token
    url = "http://image_service:8002/images?token=invalid_token"
    
    # Perform the POST request with an invalid token
    async with httpx.AsyncClient() as client:
        response_post = await client.post(url, files={'file': ('fake.jpg', b'fake content', 'image/jpeg')})
        assert response_post.status_code == 401  # Expecting Unauthorized access

    # Perform the DELETE request with an invalid token
    async with httpx.AsyncClient() as client:
        response_delete = await client.delete(url)
        assert response_delete.status_code == 401  # Expecting Unauthorized access
