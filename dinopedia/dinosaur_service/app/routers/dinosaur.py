from typing import Optional
import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db
from app.dependencies import dev_role, admin_role

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/dinosaurs", response_model=schemas.Dinosaur)
async def create_dinosaur(
    dinosaur: schemas.DinosaurCreate,
    db: Session = Depends(get_db),
    role: str = Depends(admin_role)
):
    """
    Create a new dinosaur.

    Args:
        dinosaur (schemas.DinosaurCreate): The dinosaur data.
        db (Session): The database session.
        token (str): The authentication token.

    Returns:
        schemas.Dinosaur: The created dinosaur.

    Raises:
        HTTPException: If the token is missing or the user is not an admin.
    """
    logger.info("Creating a new dinosaur with data: %s", dinosaur)
    try:
        created_dinosaur = crud.create_dinosaur(db=db, dinosaur=dinosaur)
        logger.info("Dinosaur created successfully with ID: %s", created_dinosaur.id)
        return created_dinosaur
    except Exception as e:
        logger.error("Failed to create dinosaur: %s", e)
        raise ValueError("Failed to create dinosaur", e)

@router.get("/dinosaurs")
async def get_dinosaurs(
    name: Optional[str] = Query(None),
    eating_classification: Optional[str] = Query(None),
    typical_color: Optional[str] = Query(None),
    period: Optional[str] = Query(None),
    average_size: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 10,
    include_images: bool = Query(False),
    db: Session = Depends(get_db),
    role: str = Depends(dev_role)
):
    """
    Retrieve a list of dinosaurs with optional filtering and pagination.

    Args:
        token (str): The authentication token.
        name (Optional[str]): Filter by name.
        eating_classification (Optional[str]): Filter by eating classification.
        typical_color (Optional[str]): Filter by typical color.
        period (Optional[str]): Filter by period.
        average_size (Optional[str]): Filter by average size.
        skip (int): Number of records to skip for pagination.
        limit (int): Maximum number of records to return.
        include_images (bool): Whether to include images in the response.
        db (Session): The database session.

    Returns:
        List[schemas.DinosaurWithImages or schemas.DinosaurWithoutImages]: The list of dinosaurs.

    Raises:
        HTTPException: If the token is missing or the user is not a developer.
    """
    logger.info("Fetching dinosaurs with filters: name=%s, eating_classification=%s, typical_color=%s, period=%s, average_size=%s, skip=%d, limit=%d, include_images=%s",
                name, eating_classification, typical_color, period, average_size, skip, limit, include_images)
    dinosaurs = crud.get_dinosaurs(
        db,
        name=name,
        eating_classification=eating_classification,
        typical_color=typical_color,
        period=period,
        average_size=average_size,
        skip=skip,
        limit=limit,
        include_images=include_images
    )
    logger.info("Fetched %d dinosaurs", len(dinosaurs))
    if include_images:
        return [
            schemas.DinosaurWithImages(
                name=d.name,
                eating_classification=d.eating_classification,
                typical_color=d.typical_color,
                period=d.period,
                average_size=d.average_size,
                images=d.images
            )
            for d in dinosaurs
        ]
    else:
        return [
            schemas.DinosaurWithoutImages(
                name=d.name,
                eating_classification=d.eating_classification,
                typical_color=d.typical_color,
                period=d.period,
                average_size=d.average_size
            )
            for d in dinosaurs
        ]

@router.delete("/dinosaurs/{dinosaur_id}")
async def delete_dinosaur(
    dinosaur_id: int,
    db: Session = Depends(get_db),
    role: str = Depends(admin_role)
):
    """
    Delete a dinosaur by its ID.

    Args:
        dinosaur_id (int): The ID of the dinosaur to delete.
        db (Session): The database session.
        token (str): The authentication token.

    Returns:
        dict: A message indicating the dinosaur was deleted successfully.

    Raises:
        HTTPException: If the token is missing or the user is not an admin.
    """
    logger.info("Deleting dinosaur with ID: %d", dinosaur_id)
    try:
        crud.delete_dinosaur(db, dinosaur_id=dinosaur_id)
        logger.info("Dinosaur with ID %d deleted successfully", dinosaur_id)
        return {"message": "Dinosaur deleted successfully"}
    except ValueError as e:
        logger.error("Failed to delete dinosaur with ID %d: %s", dinosaur_id, e)
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/dinosaurs/{dinosaur_id}/images", response_model=schemas.DinosaurImage)
async def add_image(
    dinosaur_id: int,
    image: schemas.DinosaurImageCreate,
    db: Session = Depends(get_db),
    role: str = Depends(admin_role)
):
    """
    Add an image to a dinosaur.

    Args:
        dinosaur_id (int): The ID of the dinosaur to add an image to.
        image (schemas.DinosaurImageCreate): The image data.
        db (Session): The database session.
        token (str): The authentication token.

    Returns:
        schemas.DinosaurImage: The created dinosaur image.

    Raises:
        HTTPException: If the token is missing or the user is not an admin.
    """
    logger.info("Adding image to dinosaur with ID: %d", dinosaur_id)
    try:
        created_image = crud.add_image(db=db, dinosaur_id=dinosaur_id, image=image)
        logger.info("Image added to dinosaur with ID: %d, image ID: %d", dinosaur_id, created_image.id)
        return created_image
    except ValueError as e:
        logger.error("Failed to add image to dinosaur with ID %d: %s", dinosaur_id, e)
        raise HTTPException(status_code=400, detail=str(e))
