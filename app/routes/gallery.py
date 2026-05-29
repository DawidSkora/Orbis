import os
from fastapi import APIRouter, HTTPException, Query
from uuid import UUID

from app.database import supabase
from app.models.gallery import GalleryPhotoCreate, GalleryPhotoUpdate

router = APIRouter()

GALLERY_BUCKET = "gallery"


def _public_image_url(storage_path: str) -> str:
    base = os.environ["SUPABASE_URL"].rstrip("/")
    path = storage_path.lstrip("/")
    return f"{base}/storage/v1/object/public/{GALLERY_BUCKET}/{path}"


def _row_to_response(row: dict) -> dict:
    return {
        "id": row["id"],
        "petName": row["pet_name"],
        "breed": row["breed"],
        "service": row["service"],
        "category": row["category"],
        "aspectRatio": row["aspect_ratio"],
        "gradientFrom": row["gradient_from"],
        "gradientTo": row["gradient_to"],
        "imageSrc": _public_image_url(row["storage_path"]),
        "sortOrder": row.get("sort_order", 0),
        "isFeatured": row.get("is_featured", False),
        "isPublished": row.get("is_published", True),
    }


@router.get("/")
def get_all(
    featured: bool | None = Query(default=None),
    category: str | None = Query(default=None),
    limit: int | None = Query(default=None, ge=1, le=100),
):
    query = (
        supabase.table("gallery_photos")
        .select("*")
        .eq("is_published", True)
        .order("sort_order")
        .order("created_at")
    )

    if featured is not None:
        query = query.eq("is_featured", featured)
    if category is not None:
        query = query.eq("category", category)
    if limit is not None:
        query = query.limit(limit)

    result = query.execute()
    return [_row_to_response(row) for row in result.data]


@router.get("/{id}")
def get_one(id: UUID):
    result = (
        supabase.table("gallery_photos")
        .select("*")
        .eq("id", str(id))
        .eq("is_published", True)
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=404, detail="Not found")
    return _row_to_response(result.data[0])


@router.post("/")
def create(photo: GalleryPhotoCreate):
    result = supabase.table("gallery_photos").insert(photo.model_dump()).execute()
    return _row_to_response(result.data[0])


@router.put("/{id}")
def update(id: str, photo: GalleryPhotoUpdate):
    data = {k: v for k, v in photo.model_dump().items() if v is not None}
    result = supabase.table("gallery_photos").update(data).eq("id", id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Not found")
    return _row_to_response(result.data[0])


@router.delete("/{id}")
def delete(id: str):
    result = supabase.table("gallery_photos").delete().eq("id", id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Not found")
    return {"deleted": id}
