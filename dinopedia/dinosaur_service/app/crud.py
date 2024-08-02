# crud.py
from typing import Optional
from sqlalchemy.orm import Session, joinedload
from app import models, schemas
from cachetools import TTLCache, cached
import logging

logger = logging.getLogger(__name__)

# Create a cache with a TTL of 60 seconds and a maximum size of 100 items
dinosaur_cache = TTLCache(maxsize=100, ttl=60)

@cached(dinosaur_cache)
def get_dinosaur(db: Session, dinosaur_id: int):
    logger.info(f"Fetching dinosaur with id: {dinosaur_id}")
    return db.query(models.Dinosaur).filter(models.Dinosaur.id == dinosaur_id).first()

@cached(dinosaur_cache)
def get_dinosaurs(
    db: Session,
    name: Optional[str] = None,
    eating_classification: Optional[str] = None,
    typical_color: Optional[str] = None,
    period: Optional[str] = None,
    average_size: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    include_images: bool = False
):
    logger.info(f"Fetching dinosaurs with filters: name={name}, eating_classification={eating_classification}, typical_color={typical_color}, period={period}, average_size={average_size}, skip={skip}, limit={limit}, include_images={include_images}")
    query = db.query(models.Dinosaur)
    
    if include_images:
        query = query.options(joinedload(models.Dinosaur.images))
    
    if name:
        query = query.filter(models.Dinosaur.name.ilike(f"%{name}%"))
    if eating_classification:
        query = query.filter(models.Dinosaur.eating_classification.ilike(f"%{eating_classification}%"))
    if typical_color:
        query = query.filter(models.Dinosaur.typical_color.ilike(f"%{typical_color}%"))
    if period:
        query = query.filter(models.Dinosaur.period.ilike(f"%{period}%"))
    if average_size:
        query = query.filter(models.Dinosaur.average_size.ilike(f"%{average_size}%"))
    
    return query.offset(skip).limit(limit).all()

def create_dinosaur(db: Session, dinosaur: schemas.DinosaurCreate):
    db_dinosaur = models.Dinosaur(
        name=dinosaur.name,
        eating_classification=dinosaur.eating_classification,
        typical_color=dinosaur.typical_color,
        period=dinosaur.period,
        average_size=dinosaur.average_size,
    )
    db.add(db_dinosaur)
    db.commit()
    db.refresh(db_dinosaur)
    for image in dinosaur.images:
        db_image = models.DinosaurImage(**image.dict(), dinosaur_id=db_dinosaur.id)
        db.add(db_image)
    db.commit()
    return db_dinosaur

def delete_dinosaur(db: Session, dinosaur_id: int):
    db_dinosaur = db.query(models.Dinosaur).filter(models.Dinosaur.id == dinosaur_id).first()
    if db_dinosaur is None:
        raise ValueError("Dino not found")
    db.delete(db_dinosaur)
    db.commit()

def add_image(db: Session, dinosaur_id: int, image: schemas.DinosaurImageCreate):
    db_image = models.DinosaurImage(**image.dict(), dinosaur_id=dinosaur_id)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

def delete_image(db: Session, image_id: int):
    db_image = db.query(models.DinosaurImage).filter(models.DinosaurImage.id == image_id).first()
    if db_image is None:
        raise ValueError("Image not found")
    db.delete(db_image)
    db.commit()
