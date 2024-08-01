from app import models, schemas
from sqlalchemy.orm import Session

def add_image(db: Session, dinosaur_id: int, image: schemas.DinosaurImageCreate):
    # Ensure the dinosaur has fewer than 2 images
    db_dinosaur = db.query(models.Dinosaur).filter(models.Dinosaur.id == dinosaur_id).first()
    if db_dinosaur is None:
        raise ValueError("dinosaur not exist")
    if len(db_dinosaur.images) >= 2:
        raise ValueError("A dinosaur can have at most 2 images")

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

def get_images_by_dinosaur(db: Session, dinosaur_id: int):
    return db.query(models.DinosaurImage).filter(models.DinosaurImage.dinosaur_id == dinosaur_id).all()
