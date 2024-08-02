from fastapi import FastAPI
from app.routers import image
from app.database import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(image.router)

