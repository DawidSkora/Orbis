from pydantic import BaseModel
from typing import Optional, Literal

GalleryCategory = Literal["Strzyżenie", "Trymowanie", "Czesanie", "Przed & Po"]
AspectRatio = Literal["square", "portrait", "tall"]


class GalleryPhotoCreate(BaseModel):
    pet_name: str
    breed: str
    service: str
    category: GalleryCategory
    aspect_ratio: AspectRatio
    gradient_from: str
    gradient_to: str
    storage_path: str
    sort_order: int = 0
    is_featured: bool = False
    is_published: bool = True


class GalleryPhotoUpdate(BaseModel):
    pet_name: Optional[str] = None
    breed: Optional[str] = None
    service: Optional[str] = None
    category: Optional[GalleryCategory] = None
    aspect_ratio: Optional[AspectRatio] = None
    gradient_from: Optional[str] = None
    gradient_to: Optional[str] = None
    storage_path: Optional[str] = None
    sort_order: Optional[int] = None
    is_featured: Optional[bool] = None
    is_published: Optional[bool] = None
