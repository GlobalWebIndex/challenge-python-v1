from typing import List, Optional
from pydantic import BaseModel

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
    Base model for Dinosaur, containing essential attributes of a dinosaur.

    Attributes:
        name (str): The name of the dinosaur.
        eating_classification (str): The eating classification of the dinosaur.
        typical_color (str): The typical color of the dinosaur.
        period (str): The geological period in which the dinosaur lived.
        average_size (str): The average size of the dinosaur.
    """
    name: str
    eating_classification: str
    typical_color: str
    period: str
    average_size: str

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

class DinosaurWithImages(DinosaurBase):
    """
    Model representing a Dinosaur with its associated images.

    Attributes:
        images (List[DinosaurImage]): A list of images associated with the dinosaur.
    """
    images: List[DinosaurImage] = []

    class Config:
        orm_mode = True

class DinosaurWithoutImages(DinosaurBase):
    """
    Model representing a Dinosaur without its associated images.
    """
    class Config:
        orm_mode = True
