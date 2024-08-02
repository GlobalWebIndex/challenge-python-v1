import time
import pytest
import httpx

@pytest.mark.asyncio
async def test_create_dinosaur():
    # Delay the test for 2 seconds to ensure service startup
    time.sleep(2)
    # Define the URL and the payload for the POST request
    url = "http://dinosaur_service:8001/dinosaurs?token=456"
    data = {
        "name": "Tyrannosaurus Rex",
        "eating_classification": "carnivores",
        "typical_color": "green",
        "period": "cretaceous",
        "average_size": "large",
        "images": []
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data)
        # Assert the response status code and content
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["name"] == "Tyrannosaurus Rex"
        assert response_data["eating_classification"] == "carnivores"
        assert response_data["typical_color"] == "green"
        assert response_data["period"] == "cretaceous"
        assert response_data["average_size"] == "large"
        assert response_data["images"] == []
