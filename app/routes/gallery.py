from fastapi import APIRouter, HTTPException, Query
from uuid import UUID

from app.database import supabase
from app.gallery_shared import row_to_response

router = APIRouter()


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
    return [row_to_response(row) for row in result.data]


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
    return row_to_response(result.data[0])
