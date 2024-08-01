FROM python:3.10.2-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml ./
RUN apt-get update && apt-get install -y libpq-dev gcc curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    /root/.local/bin/poetry config virtualenvs.create false && \
    /root/.local/bin/poetry install

# Copy the application code
COPY . /app

# Generate poetry.lock file during the build process
RUN /root/.local/bin/poetry lock


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]

