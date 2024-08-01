from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class DinosaurImage(Base):
    __tablename__ = 'dinosaur_images'

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    dinosaur_id = Column(Integer, ForeignKey('dinosaurs.id'), nullable=False)

    dinosaur = relationship("Dinosaur", back_populates="images")

class Dinosaur(Base):
    __tablename__ = 'dinosaurs'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    images = relationship("DinosaurImage", back_populates="dinosaur", cascade="all, delete-orphan")

