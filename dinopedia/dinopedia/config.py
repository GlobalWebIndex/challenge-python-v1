import os


DATABASE_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
DATABASE_NAME: str = os.getenv("POSTGRES_DB", "dinopedia")
DATABASE_PORT: int = os.getenv("POSTGRES_PORT", 5432)
DATABASE_USER: str = os.getenv("POSTGRES_USER", "postgres")
DATABASE_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
