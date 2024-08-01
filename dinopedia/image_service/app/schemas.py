from pydantic import BaseModel
from typing import List, Optional

class DinosaurImageBase(BaseModel):
    """
    Base model for DinosaurImage, containing the URL of the image.

    Attributes:
        url (str): The URL of the image.
    """
    url: str

class DinosaurImageCreate(DinosaurImageBase):
    """
    Model for creating a DinosaurImage, inheriting from DinosaurImageBase.
    """
    pass

class DinosaurImage(DinosaurImageBase):
    """
    Model representing a DinosaurImage, including the image ID.

    Attributes:
        id (int): The unique identifier of the image.
    """
    id: int

    class Config:
        orm_mode = True

class DinosaurBase(BaseModel):
    """
    Base model for Dinosaur, containing the name of the dinosaur.

    Attributes:
        name (str): The name of the dinosaur.
    """
    name: str

class DinosaurCreate(DinosaurBase):
    """
    Model for creating a Dinosaur, inheriting from DinosaurBase and including images.

    Attributes:
        images (Optional[List[DinosaurImageCreate]]): A list of images associated with the dinosaur.
    """
    images: Optional[List[DinosaurImageCreate]] = []

class Dinosaur(DinosaurBase):
    """
    Model representing a Dinosaur, including the dinosaur ID and associated images.

    Attributes:
        id (int): The unique identifier of the dinosaur.
        images (List[DinosaurImage]): A list of images associated with the dinosaur.
    """
    id: int
    images: List[DinosaurImage] = []

    class Config:
        orm_mode = True

class DinosaurUpdate(BaseModel):
    """
    Model for updating a Dinosaur, allowing partial updates of name and images.

    Attributes:
        name (Optional[str]): The name of the dinosaur.
        images (Optional[List[DinosaurImageCreate]]): A list of images associated with the dinosaur.
    """
    name: Optional[str] = None
    images: Optional[List[DinosaurImageCreate]] = None
