import asyncio
import time
import httpx
import pytest


@pytest.mark.asyncio
async def test_get_dinosaurs_with_images():
    # Delay the test for 2 seconds to ensure service startup
    time.sleep(2)
    url = "http://dinosaur_service:8001/dinosaurs?name=Tyranno&token=123&include_images=true"
    async with httpx.AsyncClient() as client:
        max_retries = 5
        for attempt in range(max_retries):
            try:
                response = await client.get(url)
                response.raise_for_status()
                assert response.status_code == 200
                dinosaurs = response.json()
                for dinosaur in dinosaurs:
                    assert "images" in dinosaur
                break
            except (httpx.HTTPStatusError, httpx.ConnectError) as exc:
                if attempt == max_retries - 1:
                    pytest.fail(f"HTTP request failed after {max_retries} attempts: {exc}")
                await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(test_get_dinosaurs_with_images())
