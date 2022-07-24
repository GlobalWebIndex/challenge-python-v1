import requests
from requests.auth import HTTPBasicAuth

endpoint = "http://127.0.0.1:8000/api/dinosaurs"
image_location = "/home/nioannou/projects/projects/python_based/django_based/gwi_based/challenge-python-v1/images_to_test/scott-greer-XfQ3t7AGTv0-unsplash.jpg"
dinosaur_id = 3
files = {
    "image": open(image_location, "rb"),
}
# headers = { 'content-type': 'application/vnd.api+json' } TODO: I think headers are not needed
headers = {'Allow': 'GET, HEAD, OPTIONS, PATCH'}
url1 = f"{endpoint}/{dinosaur_id}/image1"
response = requests.patch(url1, files=files, auth = HTTPBasicAuth('admin', 'admin'), headers=headers)
print(response)