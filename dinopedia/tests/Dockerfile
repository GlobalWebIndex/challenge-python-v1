# tests/Dockerfile
FROM python:3.10

WORKDIR /app

COPY requirements.txt ./
COPY conftest.py ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip list

COPY test_dinosaur_service /app/test_dinosaur_service
COPY test_image_service /app/test_image_service
COPY test_user_service /app/test_user_service
CMD ["pytest", "--maxfail=1", "--disable-warnings", "--tb=short"]

