from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

from app.models.gallery import AspectRatio, GalleryCategory


class AdminGalleryBody(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    pet_name: str = Field(alias="petName")
    breed: str
    service: str
    category: GalleryCategory
    aspect_ratio: AspectRatio = Field(alias="aspectRatio")
    gradient_from: str = Field(alias="gradientFrom")
    gradient_to: str = Field(alias="gradientTo")
    storage_path: str = Field(alias="storagePath")
    sort_order: int = Field(default=0, alias="sortOrder")
    is_featured: bool = Field(default=False, alias="isFeatured")
    is_published: bool = Field(default=True, alias="isPublished")


class AdminGalleryUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    pet_name: Optional[str] = Field(default=None, alias="petName")
    breed: Optional[str] = None
    service: Optional[str] = None
    category: Optional[GalleryCategory] = None
    aspect_ratio: Optional[AspectRatio] = Field(default=None, alias="aspectRatio")
    gradient_from: Optional[str] = Field(default=None, alias="gradientFrom")
    gradient_to: Optional[str] = Field(default=None, alias="gradientTo")
    storage_path: Optional[str] = Field(default=None, alias="storagePath")
    sort_order: Optional[int] = Field(default=None, alias="sortOrder")
    is_featured: Optional[bool] = Field(default=None, alias="isFeatured")
    is_published: Optional[bool] = Field(default=None, alias="isPublished")
