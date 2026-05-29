from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.database import supabase
from app.deps.auth import require_admin
from app.gallery_shared import GALLERY_BUCKET, public_image_url, row_to_response
from app.models.admin_gallery import AdminGalleryBody, AdminGalleryUpdate

router = APIRouter(dependencies=[Depends(require_admin)])


@router.get("/")
def list_all():
    result = (
        supabase.table("gallery_photos")
        .select("*")
        .order("sort_order")
        .order("created_at")
        .execute()
    )
    return [row_to_response(row) for row in result.data]


@router.post("/")
def create(photo: AdminGalleryBody):
    data = photo.model_dump(by_alias=False)
    result = supabase.table("gallery_photos").insert(data).execute()
    return row_to_response(result.data[0])


@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing filename")

    content = await file.read()
    content_type = file.content_type or "image/webp"

    supabase.storage.from_(GALLERY_BUCKET).upload(
        file.filename,
        content,
        file_options={"content-type": content_type, "upsert": "true"},
    )

    return {
        "storagePath": file.filename,
        "imageSrc": public_image_url(file.filename),
    }


@router.put("/{id}")
def update(id: UUID, photo: AdminGalleryUpdate):
    data = {
        k: v
        for k, v in photo.model_dump(by_alias=False).items()
        if v is not None
    }
    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")
    result = supabase.table("gallery_photos").update(data).eq("id", str(id)).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Not found")
    return row_to_response(result.data[0])


@router.delete("/{id}")
def delete(id: UUID):
    result = supabase.table("gallery_photos").delete().eq("id", str(id)).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Not found")
    return {"deleted": str(id)}
