import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db
from app.dependencies import admin_role

router = APIRouter()

UPLOAD_DIRECTORY = "./uploaded_images/"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@router.post("/images", response_model=schemas.DinosaurImage)
async def upload_image(
    dinosaur_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    role: str = Depends(admin_role)
):
    """
    Upload an image for a specified dinosaur.

    Args:
        dinosaur_id (int): The ID of the dinosaur.
        file (UploadFile): The image file to upload.
        db (Session): The database session.
        role (str): The user's role, validated by the dependency.

    Returns:
        schemas.DinosaurImage: The created dinosaur image.

    Raises:
        HTTPException: If the user is not an admin.
    """
    file_location = f"{UPLOAD_DIRECTORY}/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(file.file.read())
    image_data = schemas.DinosaurImageCreate(url=file_location)
    try:
        return crud.add_image(db=db, dinosaur_id=dinosaur_id, image=image_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/images/{image_id}")
async def delete_image(
    image_id: int,
    db: Session = Depends(get_db),
    role: str = Depends(admin_role)
):
    """
    Delete an image by its ID.

    Args:
        image_id (int): The ID of the image to delete.
        db (Session): The database session.
        role (str): The user's role, validated by the dependency.

    Returns:
        dict: A message indicating the image was deleted successfully.

    Raises:
        HTTPException: If the user is not an admin.
    """
    try:
        crud.delete_image(db, image_id=image_id)
        return {"message": "Image deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/images")
async def delete_all_images_for_dinosaur(
    dinosaur_id: int,
    db: Session = Depends(get_db),
    role: str = Depends(admin_role)
):
    """
    Delete all images for a specified dinosaur.

    Args:
        dinosaur_id (int): The ID of the dinosaur.
        db (Session): The database session.
        role (str): The user's role, validated by the dependency.

    Returns:
        dict: A message indicating all images were deleted successfully.

    Raises:
        HTTPException: If the user is not an admin or no images are found.
    """
    images = crud.get_images_by_dinosaur(db, dinosaur_id=dinosaur_id)
    if not images:
        raise HTTPException(status_code=404, detail="No images found for the specified dinosaur")
    for image in images:
        file_location = image.url
        if os.path.exists(file_location):
            os.remove(file_location)
        crud.delete_image(db, image_id=image.id)
    return {"message": "All images deleted successfully"}
