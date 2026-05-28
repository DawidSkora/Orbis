from fastapi import APIRouter, HTTPException, Query
from uuid import UUID
from app.database import supabase
from app.models.qa import QAPair, QAPairUpdate

router = APIRouter()

@router.get("/")
def get_all(
    limit: int | None = Query(default=None, ge=1, le=50),
):
    query = supabase.table("qa_pairs").select("*")
    if limit is not None:
        query = query.limit(limit)

    result = query.execute()
    return result.data

@router.get("/{id}")
def get_one(id: UUID):
    result = supabase.table("qa_pairs").select("*").eq("id", str(id)).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Not found")
    return result.data[0]

@router.post("/")
def create(pair: QAPair):
    result = supabase.table("qa_pairs").insert(pair.model_dump()).execute()
    return result.data[0]

@router.put("/{id}")
def update(id: str, pair: QAPairUpdate):
    data = {k: v for k, v in pair.model_dump().items() if v is not None}
    result = supabase.table("qa_pairs").update(data).eq("id", id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Not found")
    return result.data[0]

@router.delete("/{id}")
def delete(id: str):
    result = supabase.table("qa_pairs").delete().eq("id", id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Not found")
    return {"deleted": id}