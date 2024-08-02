from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Dinosaur(Base):
    __tablename__ = 'dinosaurs'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    eating_classification = Column(String)
    typical_color = Column(String)
    period = Column(String)
    average_size = Column(String)
    images = relationship("DinosaurImage", back_populates="dinosaur")

class DinosaurImage(Base):
    __tablename__ = 'dinosaur_images'

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    dinosaur_id = Column(Integer, ForeignKey('dinosaurs.id'))
    dinosaur = relationship("Dinosaur", back_populates="images")

