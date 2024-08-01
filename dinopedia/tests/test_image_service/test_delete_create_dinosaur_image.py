import pytest
import httpx

@pytest.mark.asyncio
async def test_delete_create_dinosaur_images():
    # Create a dinosaur and get its ID
    url = "http://dinosaur_service:8001/dinosaurs?token=456"
    data = {
        "name": "Tyrannosaurus Rex",
        "eating_classification": "carnivores",
        "typical_color": "green",
        "period": "cretaceous",
        "average_size": "large",
        "images": []
    }

    # Create an instance of AsyncClient and make the POST request within an async context
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data)
    created_dinosaur = response.json()
    dinosaur_id = created_dinosaur['id']
    # Define the URLs
    delete_images_url = "http://image_service:8002/images?dinosaur_id="+str(dinosaur_id)+"&token=456"
    delete_dinosaur_url="http://dinosaur_service:8001/dinosaurs/"+str(dinosaur_id)+"?token=456"
    upload_image_url = "http://image_service:8002/images?dinosaur_id="+str(dinosaur_id)+"&token=456"
    file_path = "test_image_service/test_file.jpg"

    # Clear images for test dinosaur
    async with httpx.AsyncClient() as client:
        delete_response = await client.delete(delete_images_url)
    # add 1st Image
    with open(file_path, "rb") as f:
        files = {"file": file_path}
        async with httpx.AsyncClient() as client:
            response = await client.post(upload_image_url, files=files)
        assert response.status_code == 200 or response.status_code == 201
    # Add 2nd image
    with open(file_path, "rb") as f:
        files = {"file": file_path}
        async with httpx.AsyncClient() as client:
            response = await client.post(upload_image_url, files=files)
        assert response.status_code == 200 or response.status_code == 201
    # Add 3rd Image (should fail)
    with open(file_path, "rb") as f:
        files = {"file": file_path}
        async with httpx.AsyncClient() as client:
            response = await client.post(upload_image_url, files=files)
    # Test the image Limit
        assert response.status_code == 400
        assert response.json() == {"detail": "A dinosaur can have at most 2 images"}
    # Clear Test Data
    async with httpx.AsyncClient() as client:
        delete_response = await client.delete(delete_images_url)
        assert delete_response.status_code == 200
    # Clear Test Data
    async with httpx.AsyncClient() as client:
        delete_dinosaur_response = await client.delete(delete_dinosaur_url)
        assert delete_dinosaur_response.status_code == 200
