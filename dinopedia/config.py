import os


DATABASE_HOST: str = os.getenv("POSTGRES_HOST", "db")
DATABASE_NAME: str = os.getenv("POSTGRES_DB", "postgres")
DATABASE_PORT: int = os.getenv("POSTGRES_PORT", 5432)
DATABASE_USER: str = os.getenv("POSTGRES_USER", "postgres")
DATABASE_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
