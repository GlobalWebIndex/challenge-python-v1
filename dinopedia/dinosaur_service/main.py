from fastapi import FastAPI
from app.routers import dinosaur
from app.database import engine, Base
from app.logging_config import setup_logging

setup_logging()

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(dinosaur.router)
