# conftest.py
import pytest
from httpx import AsyncClient

@pytest.fixture(scope="module")
async def dinosaur_client():
    # Create an instance of the HTTP client
    async with AsyncClient(base_url="http://localhost:8001") as client:
        yield client

